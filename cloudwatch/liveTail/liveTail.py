import boto3
import time
import click
from datetime import datetime
from pynput import keyboard

cloudwatch = boto3.client('logs')
stop_stream = False

def on_press(key):
    global stop_stream
    stop_stream = True
    return False


def get_cloudwatch_log_groups():
    kwargs = {"limit": 50}
    cloudwatch_log_groups = []

    while True:  # Paginate
        response = cloudwatch.describe_log_groups(**kwargs)

        cloudwatch_log_groups += [(log_group["logGroupName"],log_group["arn"]) for log_group in response["logGroups"]]

        if "NextToken" in response:
            kwargs["NextToken"] = response["NextToken"]
        else:
            break
    return cloudwatch_log_groups





#add optional filter pattern
def start_tail(arn):
     global stop_stream
     start_time = time.time()
     try:
         response = cloudwatch.start_live_tail(
             logGroupIdentifiers=[arn],
             #logEventFilterPattern=filter_pattern
         )
         event_stream = response['responseStream']
         listener = keyboard.Listener(on_press=on_press)
         listener.start()

         # Handle the events streamed back in the response
         for event in event_stream:
             # This will end the Live Tail session.
             if (stop_stream):
                 event_stream.close()
                 break
             # Handle when session is started
             if 'sessionStart' in event:
                 session_start_event = event['sessionStart']
                 print(session_start_event)
             # Handle when log event is given in a session update
             elif 'sessionUpdate' in event:
                 log_events = event['sessionUpdate']['sessionResults']
                 for log_event in log_events:
                     print('[{date}] {log}'.format(date=datetime.fromtimestamp(log_event['timestamp']/1000),log=log_event['message']))
             else:
                 # On-stream exceptions are captured here
                 raise RuntimeError(str(event))
     except Exception as e:
         print(e)
     finally:
        listener.stop()


def initCli(logs):
    result = [{'name': name, 'arn': arn[:-2]} for  (name, arn) in logs]

    click.secho("\nAvaiable Cloudwatch groups:\n")
    for idx, el in enumerate(result):
        click.secho(f"{idx + 1} - {el['name']}")

    @click.command()
    @click.option('--option', prompt='\nSelect an option', type=int, help='Select an option')
    def cli(option):
        if option == 0 or option > len(result):
            return  click.secho(f"Invalid option" , fg='red')
        click.secho("Listening for new events logs ...")
        start_tail(result[option-1]['arn'])

    cli()

if __name__ == "__main__":
     logs=get_cloudwatch_log_groups()
     initCli(logs)
