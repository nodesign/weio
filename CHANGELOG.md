WeIO 1.1, not released yet
-------------------
- IDE
 - Improved the console output [[#143](https://github.com/nodesign/weio/pull/143)]
 - Improved the preview [[#146](https://github.com/nodesign/weio/pull/146)]
 - Added an option to enable/disable the login requirement to access the IDE [[#149](https://github.com/nodesign/weio/pull/149)]
 - Improved the way new projects are created [[#156](https://github.com/nodesign/weio/pull/156)]
 - Added an auto-save function [[b99325f](https://github.com/nodesign/weio/commit/b99325f78c02ed27189bc13bb42c01ea57b94564)]
 - Fixed dashboard preview on lower resolution [[#166](https://github.com/nodesign/weio/pull/166)]
 - Improved the pin visualization [[#166](https://github.com/nodesign/weio/pull/166)] [[6651fc8](https://github.com/nodesign/weio/commit/6651fc8472eafc8e7eb555435e9aa345e0136b2d)]
 - Fixed a bug with duplication [[#104](https://github.com/nodesign/weio/issues/104)] [[#179](https://github.com/nodesign/weio/pull/179)]
 - Added support for creating / editing shell scripts [[2740a52](https://github.com/nodesign/weio/commit/2740a526e458ee3910dbbc7d8cb0c66bb871a3e8)]
 - Added a logo at login screen [[7472dad](https://github.com/nodesign/weio/commit/7472dad7f1c2674a54740509aa66618f44f68b08)]
 - Examples can't be deleted anymore [[#184](https://github.com/nodesign/weio/pull/184)]
 - Updated ACE editor to v1.1.9 [[#183](https://github.com/nodesign/weio/pull/183)]
 - Enable file reopening from the file list [[#183](https://github.com/nodesign/weio/pull/183)]
 - main.py is not required anymore on pure HTML projects [[#181](https://github.com/nodesign/weio/pull/181)]

- API
  - Added a debounce time parameter for interrupts [[d2a9fe2](https://github.com/nodesign/weio/commit/d2a9fe2ca3153ad3a22f53810a047d6958fb9f89)]
  - Added support for interrupts in javascript [[6c310db](https://github.com/nodesign/weio/commit/6c310db6e5b4d713d9e8666e7610d43f5b8a6886)]
  - Fixed a bug with detachInterrupt function [[#158](https://github.com/nodesign/weio/pull/158)]
  - Fixed the initSerial parameters [[0aedb88](https://github.com/nodesign/weio/commit/0aedb8842254a1da21be7f811ead0e0d4ee9d381)]
  - Improved stability of IoTPy [[#148](https://github.com/nodesign/weio/pull/148)]
  - Improved the way the LPC is detected by IoTPy [[#163](https://github.com/nodesign/weio/pull/163)]
  - Added support for DS18B20 sensors [[#165](https://github.com/nodesign/weio/pull/165)]

- System
  - Support for bluetooth + bluez [[3736872](https://github.com/nodesign/weio/commit/3736872b7d50c9e07f45133f6df1267c954b8b1c)]
  - Update of NTPD timezones [[#144](https://github.com/nodesign/weio/pull/144)]
  - Improved samba behavior [[#149](https://github.com/nodesign/weio/pull/159)]   [[#164](https://github.com/nodesign/weio/pull/164)]
  - Added hotplug2 rules to symlink /dev/ttyACM0 and /dev/ttyACM1 [[#163](https://github.com/nodesign/weio/pull/163)]

- Examples
  - Fixed webCamSinglePhotoWEB example [[0c18062](https://github.com/nodesign/weio/commit/0c180625e096767da8ed0b1ad9f38fd76bf5e611)]
  - Added twitter_PY example [[#139](https://github.com/nodesign/weio/pull/139)]
  - Added interrupt_JS example [[3ef5b1d](https://github.com/nodesign/weio/commit/3ef5b1ddc7d5093c1ac7a8cd5494f5ea86e4169d)]
  - Added an example for the DS18B20 temperature sensor [[#165](https://github.com/nodesign/weio/pull/165)]
  - Added an example to play wave files [[c786e8d](https://github.com/nodesign/weio/commit/c786e8d12e74b82a44c1f1cd481397f27db62a55)]
  - Added an example to play internet radio [[ed10165](https://github.com/nodesign/weio/commit/ed101654b08357e2891450fe45268e20b42f7d73)]
  - Added examples for bluetooth [[dea3107](https://github.com/nodesign/weio/commit/dea3107e73ce8e3c81f55badaa568286459dc9ad)]
  - Fixed a bug with DTHxx example [[#192](https://github.com/nodesign/weio/pull/192)]


WeIO 1.0, 2015/02/04
--------------------
- Initial release
