import serial
import argparse

import logging
 
from waggle.plugin import Plugin, get_timestamp

def parse_values(sample, **kwargs):
    # Note: Sonic has an incoming string 
    data_raw = str(sample,'utf-8').strip()
    #print(data_raw)
    try:
        wx = data_raw.split(";")[1]
        wy = data_raw.split(";")[2]
        wz = data_raw.split(";")[3]
        temp1 = data_raw.split(";")[4]
        parms = ['U','V','W','T']
        data =  [wx, wy, wz, temp1]
        # Convert the variables to floats
        strip = [float(var) for var in data]
        # Create a dictionary to match the parameters and variables
        ndict = dict(zip(parms, strip))
        # Add the AQT datetime to the dictionary
        #print(ndict)
        return ndict
    except:
        print("no wind data")
        return False


def start_publishing(args, plugin, dev, **kwargs):
    """
    start_publishing initializes the Visala WXT530
    Begins sampling and publishing data

    Functions
    ---------


    Modules
    -------
    plugin
    logging
    sched
    parse
    """
    # Note: AQT ASCII interface configuration described in manual
    line = dev.readline()
    # Note: AQT has 1 min data output, need to check if bytes are returned
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
                for key, name in kwargs['names'].items():
                    try:
                        value = sample[key]
                    except KeyError:
                        continue
                    # Update the log
                    if kwargs.get('debug', 'False'):
                        print('node', timestamp, name, value, kwargs['units'][name], type(value))
                    
                    logging.info("node publishing %s %s units %s type %s", name, value, kwargs['units'][name], str(type(value)))
                    plugin.publish(name,
                                   value=value,
                                   meta={"units" : kwargs['units'][name],
                                         "sensor" : "metek-sonic3D",
                                         "missing" : '-9999.9',
                                         "description" : kwargs['description'][name]
                                         },
                                   scope="node",
                                   timestamp=timestamp
                                   )
            # setup and publish to the beehive                        
            if kwargs['beehive_interval'] > 0:
                # publish each value in sample
                for key, name in kwargs['names'].items():
                    try:
                        value = sample[key]
                    except KeyError:
                        continue
                    # Update the log
                    if kwargs.get('debug', 'False'):
                        print('beehive', timestamp, name, value, kwargs['units'][name], type(value))

                    logging.info("beehive publishing %s %s units %s type %s", name, value, kwargs['units'][name], str(type(value)))
                    plugin.publish(name,
                                   value=value,
                                   meta={"units" : kwargs['units'][name],
                                         "sensor" : "METEK-sonic3D",
                                         "missing" : '-9999.9',
                                         "description" : kwargs['description'][name]
                                        },
                                   scope="beehive",
                                   timestamp=timestamp
                                  )

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
                print("keyboard interrupt")
                print(e)
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
    args = parser.parse_args()


    main(args)
