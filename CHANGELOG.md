WeIO 1.1, not released yet
-------------------
- IDE
 - Improved the console output [[#143](https://github.com/nodesign/weio/pull/143)]
 - Improved the preview [[#146](https://github.com/nodesign/weio/pull/146)]
 - Added an option to enable/disable the login requirement to access the IDE [[#149](https://github.com/nodesign/weio/pull/149)]
 - Improved the way new projects are created [[#156](https://github.com/nodesign/weio/pull/156)]

- API
  - Added a debounce time parameter for interrupts [[d2a9fe2](https://github.com/nodesign/weio/commit/d2a9fe2ca3153ad3a22f53810a047d6958fb9f89)]
  - Added support for interrupts in javascript [[6c310db](https://github.com/nodesign/weio/commit/6c310db6e5b4d713d9e8666e7610d43f5b8a6886)]
  - Fixed a bug with detachInterrupt function [[#158](https://github.com/nodesign/weio/pull/158)]
  - Fixed the initSerial parameters [[0aedb88](https://github.com/nodesign/weio/commit/0aedb8842254a1da21be7f811ead0e0d4ee9d381)]
  - Improved stability of IoTPy [[#148](https://github.com/nodesign/weio/pull/148)]
  - Improved the way the LPC is detected by IoTPy [[#163](https://github.com/nodesign/weio/pull/163)]

- System
  - Support for bluetooth + bluez [[3736872](https://github.com/nodesign/weio/commit/3736872b7d50c9e07f45133f6df1267c954b8b1c)]
  - Update of NTPD timezones [[#144](https://github.com/nodesign/weio/pull/144)]
  - Improved samba behavior [[#149](https://github.com/nodesign/weio/pull/159)]   [[#164](https://github.com/nodesign/weio/pull/164)]
  - Added hotplug2 rules to symlink /dev/ttyACM0 and /dev/ttyACM1 [[#163](https://github.com/nodesign/weio/pull/163)]

- Examples
  - Fixed webCamSinglePhotoWEB example [[0c18062](https://github.com/nodesign/weio/commit/0c180625e096767da8ed0b1ad9f38fd76bf5e611)]
  - Added twitter_PY example [[#139](https://github.com/nodesign/weio/pull/139)]
  - Added interrupt_JS example [[3ef5b1d](https://github.com/nodesign/weio/commit/3ef5b1ddc7d5093c1ac7a8cd5494f5ea86e4169d)]


WeIO 1.0, 2015/02/04
--------------------
- Initial release
