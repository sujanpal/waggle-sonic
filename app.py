import serial
import argparse
import logging
from waggle.plugin import Plugin, get_timestamp
import time
import sys

def parse_values(data_string):
    ''' Extracts values (e.g. 'U', 'V', 'W', 'T') from a data string
     and returns them as a dictionary if successful, else returns `False`.
    '''
    # Note: Sonic has an incoming string 
    data_raw = str(data_string,'utf-8').strip()
    try:
        # Assumes values be in same order.
        parms = ['U', 'V', 'W', 'T']
        data = data_raw.split(";")[1:5]

        # Convert the variables from string to floats
        strip = [float(var) for var in data]
        # Create a dictionary to match the parameters and variables
        sample = dict(zip(parms, strip))
        return sample
    except:
        return False
        #print("no wind data")

def publish_data(plugin, sample, timestamp, scope, kwargs_dict):
    ''' Retrieves the values from sample, 
    and publishes the data with metadata 
    to the specified scope using the `plugin.publish`.
    '''
    for key, name in kwargs_dict['names'].items():
        try:
            value = sample[key]
        except KeyError:
            plugin.publish('status', 'KeyError', meta={'var': key})
            continue
        if kwargs_dict.get('debug', False):
            print(scope, timestamp, name, value, kwargs_dict['units'][name], type(value))
        logging.info("%s publishing %s %s units %s type %s", scope, name, value, kwargs_dict['units'][name], str(type(value)))
        plugin.publish(name,
                        value=value,
                        meta={
                            "units": kwargs_dict['units'][name],
                            "sensor": "metek-sonic3D",
                            "missing": '-9999.9',
                            "description": kwargs_dict['description'][name]
                        },
                        scope=scope,
                        timestamp=timestamp
                        )

def start_publishing(args, plugin, dev, **kwargs):
    """
    Initializes the Visala WXT530,
    begins sampling and calls `publish_data`.
    """
    # Note: METEK Sonic ASCII interface configuration described in manual
    line = dev.readline()
    if len(line) > 0: 
        # Define the timestamp
        timestamp = get_timestamp()
        logging.debug("Read transmitted data")
        # Check for valid command
        sample = parse_values(line)
    
        # If valid parsed values, send to publishing
        if sample:
            # setup and publish to the node
            if kwargs['node_interval'] > 0:
                # publish each value in sample
                publish_data(plugin, sample, timestamp, 'node', kwargs)
                #print("published at node")
 
            # setup and publish to the beehive                        
            if kwargs['beehive_interval'] > 0:
                publish_data(plugin, sample, timestamp, 'beehive', kwargs)
                #print("published at beehive")
        else:
            plugin.publish('status', 'parsing_error')
            time.sleep(args.wait)
    else:
        plugin.publish('status', 'device_error')
        sys.exit(-1)



def main(args):
    publish_names = {"T": "sonic3d.temp",
                    "U": "sonic3d.uwind",
                    "V": "sonic3d.vwind",
                    "W": "sonic3d.wwind",
                    }

    units = {publish_names['T'] : "degrees Celsius",
             publish_names['U'] : "m/s",
             publish_names['V'] : "m/s",
             publish_names['W'] : "m/s"
             }
    
    description = {publish_names['T'] : "Ambient Temperature",
                   publish_names['U'] : "E/W wind",
                   publish_names['V'] : "N/S wind",
                   publish_names['W'] : "Vertical wind"
                  }

    with Plugin() as plugin, serial.Serial(args.device, baudrate=args.baud_rate, timeout=1.0) as dev:
        while True:
            try:
                start_publishing(args, 
                                 plugin,
                                 dev,
                                 node_interval=args.node_interval,
                                 beehive_interval=args.beehive_interval,
                                 names=publish_names,
                                 units=units,
                                 description=description
                                 )
            except Exception as e:
                plugin.publish('status', e)
                #print("keyboard interrupt")
                #print(e)
                break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description="Plugin for Pushing Sonic 3D anemometer data through WSN")

    parser.add_argument("--debug",
                        action="store_true",
                        dest='debug',
                        help="enable debug logs"
                        )
    parser.add_argument("--device",
                        type=str,
                        dest='device',
                        default="/dev/ttyUSB2",
                        help="serial device to use"
                        )
    parser.add_argument("--baudrate",
                        type=int,
                        dest='baud_rate',
                        default=57600,
                        help="baudrate to use"
                        )
    parser.add_argument("--node-publish-interval",
                        default=1.0,
                        dest='node_interval',
                        type=float,
                        help="interval to publish data to node " +
                             "(negative values disable node publishing)"
                        )
    parser.add_argument("--beehive-publish-interval",
                        default=1.0,
                        dest='beehive_interval',
                        type=float,
                        help="interval to publish data to beehive " +
                             "(negative values disable beehive publishing)"
                        )
    parser.add_argument("--wait",
                        default=3.0,
                        dest='wait',
                        type=float,
                        help="wait for device to send the data"
                        )
    args = parser.parse_args()


    main(args)
