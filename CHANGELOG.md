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
 - Added traceback on python errors [[#208](https://github.com/nodesign/weio/pull/208)]
 - Corrected bug in preview display (server starts too late on a preview without prior PLAY) [[#227](https://github.com/nodesign/weio/pull/227)]

- API
  - Added a debounce time parameter for interrupts [[d2a9fe2](https://github.com/nodesign/weio/commit/d2a9fe2ca3153ad3a22f53810a047d6958fb9f89)]
  - Added support for interrupts in javascript [[6c310db](https://github.com/nodesign/weio/commit/6c310db6e5b4d713d9e8666e7610d43f5b8a6886)]
  - Fixed a bug with detachInterrupt function [[#158](https://github.com/nodesign/weio/pull/158)]
  - Fixed the initSerial parameters [[0aedb88](https://github.com/nodesign/weio/commit/0aedb8842254a1da21be7f811ead0e0d4ee9d381)]
  - Improved stability of IoTPy [[#148](https://github.com/nodesign/weio/pull/148)]
  - Improved the way the LPC is detected by IoTPy [[#163](https://github.com/nodesign/weio/pull/163)]
  - Added support for DS18B20 sensors [[#165](https://github.com/nodesign/weio/pull/165)]
  - Check for internet connectivity [[#213](https://github.com/nodesign/weio/pull/213)]
  - Added support for the HC-SR04 [[81c3aefa](https://github.com/nodesign/weio/commit/81c3aefa36e586a15ee046245ae31a1d95265a2a)]
  - Reduced the default interrupt debounce time from 50ms to 10ms [[#219](https://github.com/nodesign/weio/pull/219)]
  - Fixed the support for the rotary encoders [[#220](https://github.com/nodesign/weio/pull/220)]

- System
  - Support for bluetooth + bluez [[3736872](https://github.com/nodesign/weio/commit/3736872b7d50c9e07f45133f6df1267c954b8b1c)]
  - Update of NTPD timezones [[#144](https://github.com/nodesign/weio/pull/144)]
  - Improved samba behavior [[#149](https://github.com/nodesign/weio/pull/159)]   [[#164](https://github.com/nodesign/weio/pull/164)]
  - Added hotplug2 rules to symlink /dev/ttyACM0 and /dev/ttyACM1 [[#163](https://github.com/nodesign/weio/pull/163)]
  - Refactoring of the update process
  - Fixed a race condition bug in tornado [[415a3cc5](https://github.com/nodesign/weio/commit/415a3cc5f73d47a9cdce745a8c7ef9292365dcb2)]
  - Added *nano* editor [[b008bb9](https://github.com/nodesign/weio/commit/b008bb95afca910acff2a37fb19f82572f7e1d3b)]
  - Added additional webcam drivers [[7903688](https://github.com/nodesign/weio/commit/790368861af8991fb8e60e665d9d5ebfbb8f1793)]


- Examples
  - Fixed webCamSinglePhotoWEB example [[0c18062](https://github.com/nodesign/weio/commit/0c180625e096767da8ed0b1ad9f38fd76bf5e611)]
  - Added twitter_PY example [[#139](https://github.com/nodesign/weio/pull/139)]
  - Added interrupt_JS example [[3ef5b1d](https://github.com/nodesign/weio/commit/3ef5b1ddc7d5093c1ac7a8cd5494f5ea86e4169d)]
  - Added an example for the DS18B20 temperature sensor [[#165](https://github.com/nodesign/weio/pull/165)]
  - Added an example to play wave files [[c786e8d](https://github.com/nodesign/weio/commit/c786e8d12e74b82a44c1f1cd481397f27db62a55)]
  - Added an example to play internet radio [[ed10165](https://github.com/nodesign/weio/commit/ed101654b08357e2891450fe45268e20b42f7d73)]
  - Added examples for bluetooth [[dea3107](https://github.com/nodesign/weio/commit/dea3107e73ce8e3c81f55badaa568286459dc9ad)]
  - Fixed a bug with DTHxx example [[#192](https://github.com/nodesign/weio/pull/192)]
  - Added an example for the HC-SR04 [[81c3aefa](https://github.com/nodesign/weio/commit/81c3aefa36e586a15ee046245ae31a1d95265a2a)]
  - Added an example for the rotary encoder [[3079c01](https://github.com/nodesign/weio/commit/3079c017e2f9c9c319e395c586efd2196f6f34e4)]

- Firmware
  - Improved the DHTxx support (fix for the DHT22 sensor) [[#207](https://github.com/nodesign/weio/pull/207)]
  - Added the support for HC-SR04 [[#209](https://github.com/nodesign/weio/pull/209)]

WeIO 1.0, 2015/02/04
--------------------
- Initial release
