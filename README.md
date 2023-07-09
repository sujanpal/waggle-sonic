**METEK uSonic-3 3D Ultrasonic Anemometer Waggle Plugin** <br>
Waggle Sensor Plug-In for the [uSonic-3 CLASS-A MP](https://metek.de/product/usonic-3-class-a/) <br>
The Sonic 3D provides observations of 3 wind components x, y, z and acoustic temperature T at sampling rate up to 50 Hz.<br>
<br>
[Waggle sensor information](https://github.com/waggle-sensor)<br>
<br>
Build of the application was similar to the [Vaisala AQT530 plugin](https://github.com/jrobrien91/waggle-aqt)

**Access the data**<br>
import sage_data_client <br>
df = sage_data_client.query(start="2023-07-09T00:00:00Z", <br>
                            end="2023-07-09T01:00:00Z", <br>
                            filter={<br>
                                "plugin": "10.31.81.1:5000/local/waggle-sonic3d",<br>
                                "vsn": "W039",<br>
                                "sensor": "metek-sonic3D"<br>
                            }<br>
) <br>
Detailed [Cookbook](https://github.com/sujanpal/instrument-cookbooks/blob/main/notebooks/METEK_Sonic3D_access.ipynb)
