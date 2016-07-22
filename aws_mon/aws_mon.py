#!/usr/bin/env python

"""Zabbix monitor plugin for AWS

Set the path to credentials file

"""

import os
import sys
import datetime
import boto3
import argparse
import configparser

__author__ = 'Max Nogin'

AWS_CREDENTIALS_FILE = '/etc/zabbix/.aws'

service_list = {'ec2': 'InstanceId',
                'elb': 'LoadBalancerName',
                'rds': 'DBInstanceIdentifier',
                'elasticache': 'CacheClusterId'}


class Watcher:
    """Class for monitoring AWS

    Class encapsulates all methods for monitoring AWS
    """
    def __init__(self, aws_access):
        self.aws_access = aws_access
        self.metric = {'elb': 'AWS/ELB',
                       'rds': 'AWS/RDS',
                       'ec2': 'AWS/EC2',
                       'elasticache': 'AWS/ElastiCache'}

    def _list_ec2(self):
        """Get instances EC2 from AWS
        :return:
        data - dict of instances
        """
        data = {}
        ec2 = boto3.resource('ec2', **self.aws_access)
        instances = ec2.instances.all()
        for instance in instances:
            val = None
            for tag in instance.tags:
                if tag['Key'] == 'Name':
                    val = tag['Value']
            data[val]=instance.id
        return data

    def _list_elb(self):
        """Get instances ELB from AWS
        :return:
        data - dict of instances
        """
        data = {}
        client = boto3.client('elb', **self.aws_access)
        elbs = client.describe_load_balancers()['LoadBalancerDescriptions']
        for elb in elbs:
            instances = []
            for inst in elb['Instances']:
                instances.append(inst['InstanceId'])
            data[elb['LoadBalancerName']] = instances
        return data

    def _list_rds(self):
        """Get instances RDS from AWS
        :return:
        data - dict of instances
        """
        data = {}
        client = boto3.client('rds', **self.aws_access)
        rds = client.describe_db_instances()
        for instance in rds['DBInstances']:
            data[instance['DBInstanceIdentifier']] = instance['DBSubnetGroup']['VpcId']
        return data

    def _list_elasticache(self):
        """Get instances ElastiCache from AWS
        :return:
        data - dict of instances
        """
        data = {}
        client = boto3.client('elasticache', **self.aws_access)
        ec = client.describe_cache_clusters()
        for instance in ec['CacheClusters']:
            data[instance['CacheClusterId']] = 'None'
        return data

    def list_instances(self, service='ec2'):
        """Wrapper for functions to get instances EC2 from AWS
        :param service: service type
        :return:
        data - dict of instances
        """
        try:
            return getattr(self, '_list_'+service)()
        except AttributeError:
            return {}

    def list_metrics(self, service='ec2'):
        """Get metrics from AWS.
        :param service: service type

        Not all metrics are listed via API.
        ELB metrics not available:
        "HTTPCode_ELB_4XX"
        "HTTPCode_ELB_5XX"
        "BackendConnectionErrors"

        ElastiCache some metrics not listed

        :return:
        data - list of metrics
        """
        data = []
        client = boto3.client('cloudwatch', **self.aws_access)
        metrics = client.list_metrics(Namespace=self.metric[service])
        dimension = []
        for metric in metrics['Metrics']:
            if metric['Dimensions'] and not dimension:
                dimension = metric['Dimensions']
            if metric['Dimensions'] == dimension:
                data.append(metric['MetricName'])
        return data

    def _get_metric_raw(self, namespace, instance, metric, dimensions_name, period, statistic):
        """Get raw data for selected metric from AWS
        :param namespace: Namespace for AWS
        :param instance: Instance name
        :param metric: Metric name
        :param dimension_name: What we find?
        :param period: The granularity, in seconds, of the returned datapoints
        :param statistic: Statistic function
        :return:
        response - dict
        """
        cw = boto3.client('cloudwatch', **self.aws_access)
        if dimensions_name:
            response = cw.get_metric_statistics(
                Namespace=self.metric[namespace], MetricName=metric,
                StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=period*5),
                EndTime=datetime.datetime.utcnow(), Period=period,
                Statistics=[statistic],
                Dimensions=[
                    {'Name': dimensions_name, 'Value': instance},
                ])
        else:
            response = cw.get_metric_statistics(
                Namespace=self.metric[namespace], MetricName=metric,
                StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=period*5),
                EndTime=datetime.datetime.utcnow(), Period=period,
                Statistics=[statistic]
                )
        return response

    def get_metric(self, service, instance, metric, result_type='f', accuracy=4, period=60, statistic='Average'):
        """Wrapper for functions to get metric data from AWS
        :param service: Service type
        :param instance: Instance name
        :param metric: Metric name
        :param result_type: Type of result (f - float i - int)
        :param accuracy: Accuracy of the result
        :param period: The granularity, in seconds, of the returned datapoints
        :param statistic: Statistic function
        :return:
        last['Average'] - last result from API response
        """

        if service == 'ec2':
            instance_list = self._list_ec2()
            instance = instance_list[instance]
        try:
            data = self._get_metric_raw(service, instance, metric, service_list[service], period, statistic)
        except AttributeError:
            return 0
        last = []
        for result in data['Datapoints']:
            if not last:
                last = result
            elif result['Timestamp'] > last['Timestamp']:
                last = result
        if result_type == 'f':
            output_format = '%.'+str(accuracy)+result_type
        else:
            output_format = '%i'
        if last:
            return output_format % last[statistic]
        else:
            return 0


def check_aws_credentials(region):
    try:
        if os.path.exists(AWS_CREDENTIALS_FILE):
            cfg = configparser.RawConfigParser()
            cfg.read(AWS_CREDENTIALS_FILE)
            return {
                'aws_access_key_id': cfg.get('default', 'aws_access_key_id'),
                'aws_secret_access_key': cfg.get('default', 'aws_secret_access_key'),
                'region_name': region
            }
        else:
            print 'Config file not found!'
            sys.exit(1)
    except:
        print 'Error reading config file!'
        sys.exit(1)


def main():
    func_choices = ['SampleCount', 'Average', 'Sum', 'Minimum', 'Maximum']
    parser = argparse.ArgumentParser(description='Zabbix AWS plugin')
    parser.add_argument('-t', '--type', choices=service_list.keys(), help='Service type')
    parser.add_argument('-i', '--instance', metavar='NAME', help='Instance name')
    parser.add_argument('-m', '--metric', metavar='NAME', help='Metric name')
    parser.add_argument('-r', '--region', metavar='NAME', default='cn-north-1', help='Region name(Default cn-north-1)')
    parser.add_argument('-rt', '--result-type', choices=['f', 'i'], default='f', help='Result type (Default f - float)')
    parser.add_argument('-a', '--accuracy', metavar='NAME', default=4, help='Result accuracy for float (Default 4)')
    parser.add_argument('-p', '--period', metavar='NAME', default=60, help='Request range in seconds (Default 60)')
    parser.add_argument('-s', '--statistic', choices=func_choices, default='Average', help='Request function (Default Average)')
    parser.add_argument('-lm', '--list-metrics', choices=service_list.keys(), help='List available metrics')
    parser.add_argument('-li', '--list-instances', choices=service_list.keys(), help='List available instances')
    args = parser.parse_args()
    if not args.list_metrics and not args.type and not args.list_instances:
        parser.print_help()
        sys.exit(0)

    aws_access = check_aws_credentials(args.region)
    monitor = Watcher(aws_access)

    if args.list_metrics:
        print monitor.list_metrics(args.list_metrics)

    if args.list_instances:
        print monitor.list_instances(args.list_instances)

    if args.type:
        if not args.instance or not args.metric:
            parser.print_help()
            sys.exit(1)
        print monitor.get_metric(args.type, args.instance, args.metric, args.result_type, args.accuracy,
                                 int(args.period), args.statistic)


if __name__ == '__main__':
    main()


