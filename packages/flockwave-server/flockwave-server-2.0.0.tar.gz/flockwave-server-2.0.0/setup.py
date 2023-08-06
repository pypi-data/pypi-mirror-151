# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['flockwave',
 'flockwave.gateway',
 'flockwave.proxy',
 'flockwave.server',
 'flockwave.server.command_handlers',
 'flockwave.server.ext',
 'flockwave.server.ext.beacon',
 'flockwave.server.ext.crazyflie',
 'flockwave.server.ext.debug',
 'flockwave.server.ext.frontend',
 'flockwave.server.ext.http_server',
 'flockwave.server.ext.mavlink',
 'flockwave.server.ext.missions',
 'flockwave.server.ext.rtk',
 'flockwave.server.ext.show',
 'flockwave.server.ext.socketio',
 'flockwave.server.ext.socketio.vendor',
 'flockwave.server.ext.socketio.vendor.engineio_v3',
 'flockwave.server.ext.socketio.vendor.engineio_v3.async_drivers',
 'flockwave.server.ext.socketio.vendor.engineio_v4',
 'flockwave.server.ext.socketio.vendor.engineio_v4.async_drivers',
 'flockwave.server.ext.socketio.vendor.socketio_v4',
 'flockwave.server.ext.socketio.vendor.socketio_v5',
 'flockwave.server.ext.ssdp',
 'flockwave.server.ext.virtual_uavs',
 'flockwave.server.ext.webui',
 'flockwave.server.middleware',
 'flockwave.server.model',
 'flockwave.server.registries',
 'flockwave.server.tasks',
 'flockwave.server.utils',
 'skybrush']

package_data = \
{'': ['*'],
 'flockwave.server.ext.frontend': ['static/*', 'templates/*'],
 'flockwave.server.ext.webui': ['static/css/*', 'static/js/*', 'templates/*']}

install_requires = \
['adrenaline>=1.0.0,<2.0.0',
 'aio-usb-hotplug>=5.0.0,<6.0.0',
 'aiocflib>=2.5.2,<3.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'bidict>=0.19.0',
 'blinker>=1.4,<2.0',
 'click>=8.0.0,<9.0.0',
 'colour>=0.1.5',
 'compose>=1.1.1,<2.0.0',
 'crcmod>=1.7,<2.0',
 'flockwave-app-framework[daemon]>=2.4.1,<3.0.0',
 'flockwave-async>=1.3.0,<2.0.0',
 'flockwave-conn[rpc,serial]>=5.0.0,<6.0.0',
 'flockwave-ext>=1.14.3,<2.0.0',
 'flockwave-gps>=2.2.0,<3.0.0',
 'flockwave-logger>=1.8.0,<2.0.0',
 'flockwave-mavlink>=0.1.0',
 'flockwave-net[async]>=3.0.1,<4.0.0',
 'flockwave-parsers>=2.0.1,<3.0.0',
 'flockwave-spec>=1.61.0,<2.0.0',
 'httpx>=0.18.2',
 'hypercorn[trio]>=0.10.1',
 'igrf-model>=1.1.1,<2.0.0',
 'jsonschema>=4.0.3,<5.0.0',
 'msgpack>=1.0.0,<2.0.0',
 'passlib[bcrypt]>=1.7.2,<2.0.0',
 'pyjwt>=1.7.1,<2.0.0',
 'pyledctrl>=4.0.0,<5.0.0',
 'pynmea2>=1.15.0,<2.0.0',
 'pyserial>=3.4,<4.0',
 'python-baseconv>=1.2.2,<2.0.0',
 'python-dotenv>=0.14.0',
 'quart-trio>=0.9.0',
 'quart>=0.16.0',
 'trio-util>=0.5.0',
 'trio>=0.20.0']

extras_require = \
{'all': ['skybrush-ext-dock>=1.0.0,<2.0.0',
         'skybrush-ext-flockctrl>=1.0.1,<2.0.0',
         'skybrush-ext-sidekick>=1.0.0,<2.0.0',
         'skybrush-ext-timecode>=1.0.0,<2.0.0'],
 'collmot': ['skybrush-ext-dock>=1.0.0,<2.0.0',
             'skybrush-ext-flockctrl>=1.0.1,<2.0.0',
             'skybrush-ext-timecode>=1.0.0,<2.0.0'],
 'pro': ['skybrush-ext-sidekick>=1.0.0,<2.0.0',
         'skybrush-ext-timecode>=1.0.0,<2.0.0']}

entry_points = \
{'console_scripts': ['skybrush-gateway = flockwave.gateway.launcher:start',
                     'skybrush-proxy = flockwave.proxy.launcher:start',
                     'skybrushd = flockwave.server.launcher:start']}

setup_kwargs = {
    'name': 'flockwave-server',
    'version': '2.0.0',
    'description': 'Skybrush server component',
    'long_description': None,
    'author': 'Tamas Nepusz',
    'author_email': 'tamas@collmot.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
