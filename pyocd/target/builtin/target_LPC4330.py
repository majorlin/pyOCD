# pyOCD debugger
# Copyright (c) 2006-2015,2018 Arm Limited
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ...core.coresight_target import CoreSightTarget
from ...core.memory_map import (FlashRegion, RamRegion, MemoryMap)
from ...debug.svd.loader import SVDFile

FLASH_ALGO = { 'load_address' : 0x10000000,
               'instructions' : [
                        0xe00abe00, 0x062d780d, 0x24084068, 0xd3000040, 0x1e644058, 0x1c49d1fa, 0x2a001e52, 0x4770d1f2,
                        0x4770ba40, 0x4770bac0, 0xb5104935, 0x22004449, 0x604a600a, 0x608a4a33, 0x32fff04f, 0x220860ca,
                        0x4931610a, 0x60084449, 0x48304931, 0x49316708, 0x600820f3, 0x610820d3, 0x608860c8, 0x20136048,
                        0x48276148, 0x4448230c, 0x210322c0, 0xf0003880, 0x2800fb23, 0x2001d000, 0x2000bd10, 0x48204770,
                        0x44482100, 0xf1a06001, 0x68890180, 0x491d6041, 0x21046081, 0x46016101, 0xf0013880, 0x491ab890,
                        0x4449b510, 0x1a416809, 0x44484815, 0xf44f6001, 0x60415180, 0x60814913, 0x61012120, 0x38804601,
                        0xf87df001, 0xd0002800, 0xbd102001, 0x4a0e4613, 0x444ab510, 0x1a826812, 0x44484809, 0x2100e9c0,
                        0x60814908, 0x60c12100, 0x61012108, 0x46194602, 0xf0003880, 0x2800ff3e, 0x2001d000, 0xbd10,
                        0x88, 0x10080000, 0x4, 0x1000800, 0x40050000, 0x4008618c, 0x604849f9, 0xc800480,
                        0x2801d006, 0x2802d008, 0x2803d008, 0x6948d008, 0x79269ca, 0x4770d4fc, 0xe7f97d08, 0xe7f78a88,
                        0x7d0a8a88, 0x4002ea40, 0xb510e7f2, 0x1400f44f, 0x5141eb04, 0x6000ea41, 0x4002ea40, 0xbd104318,
                        0x3406a80, 0xf44fd502, 0x477010c0, 0x47702000, 0x4604b510, 0x46084613, 0x46112200, 0xffe5f7ff,
                        0x46204601, 0xffecf7ff, 0x4010e8bd, 0xe7c34308, 0xb5004bdb, 0xf7ff609a, 0x4308ffe3, 0xeb04f85d,
                        0xb530e7ba, 0x46054cd6, 0x46114608, 0x230060a3, 0xf7ff461a, 0x4601ffca, 0xf7ff4628, 0x4301ffd1,
                        0x69e06061, 0xd4fc0780, 0x2200bd30, 0xe7cf2106, 0x460db5f0, 0x461f4616, 0xf7ff4604, 0x463bfff6,
                        0x46294632, 0xe8bd4620, 0xe7da40f0, 0x460db5f0, 0x461c4616, 0xf7ff4607, 0x49c1ffe8, 0x4638608e,
                        0xffaef7ff, 0xf4404328, 0x60484000, 0xc8004a8, 0x2801d007, 0xb2a2d00b, 0xd00a2802, 0xd0042803,
                        0x69c8614c, 0xd4fc0780, 0x828abdf0, 0x750c0c24, 0x828ae7f7, 0x49b2e7f5, 0xf01369cb, 0xd0190f06,
                        0x61ca2210, 0xf01269ca, 0xd1fb0f16, 0xd511075a, 0xf40269c2, 0xf5b20260, 0xd30b0f40, 0x730a22ff,
                        0xf36f69c0, 0xf100000f, 0x60480001, 0x69c87d08, 0xd4fc0780, 0xe92d4770, 0x460541f0, 0x46882400,
                        0x21017cea, 0xf102fa01, 0x46204f9d, 0x69f9b2ce, 0xd4fc0789, 0x6c20f644, 0x45641c64, 0x2201d207,
                        0x46282105, 0xff64f7ff, 0x4230b2c0, 0x4230d0f4, 0x75284e94, 0xea5fd00a, 0xd00c0008, 0xd00c2801,
                        0xd0062802, 0xf03f1b8, 0xe008d10b, 0xe8bd4630, 0x4c8d81f0, 0x4c8de005, 0x4c8de003, 0xf04fe001,
                        0x462834ff, 0xff3cf7ff, 0x4308498a, 0x43087ce9, 0x69f86078, 0xd5020780, 0xd1fa1e64, 0xb1ece01e,
                        0x75287d38, 0xf00f1b8, 0x6ae8d01e, 0xb2c1b1e0, 0xd0172905, 0x46282201, 0xff2af7ff, 0x7568b2c0,
                        0xea106ae9, 0xd00f2f11, 0x4107f3c1, 0x2200b119, 0xf7ff4628, 0x4873ff1d, 0xe7c81c80, 0xf7ff4628,
                        0xe7c3ff7a, 0xe7eb7d28, 0xe7c02000, 0x4615b530, 0x460b4604, 0x46112200, 0xf7ff2001, 0x4601fef6,
                        0x2200462b, 0xf7ff4620, 0x6aa0ff41, 0xd5010480, 0xbd302000, 0xe8bd4620, 0x21004030, 0xb5f0e77b,
                        0x69c44605, 0x26a66a80, 0xd50b0581, 0x120f404, 0xf00f5b1, 0xf444d106, 0x61ec1400, 0xf4416a29,
                        0x62291100, 0xd5180681, 0xd5010540, 0xe0002702, 0x1d3f2701, 0x21852201, 0xf7ff4628, 0xf000fed9,
                        0x69e80307, 0x110f1c7, 0x20e0f400, 0x430340c8, 0x21812201, 0xf7ff4628, 0x6aa8fefb, 0xd00707c0,
                        0x22032300, 0x462821a3, 0xfedbf7ff, 0xd1fd1e76, 0x5142f3c4, 0x29064842, 0x21a5d304, 0xf4247301,
                        0xe0010440, 0x730121ff, 0xbdf06184, 0x4604b510, 0x6006a80, 0x2201d511, 0x4620212b, 0xfea8f7ff,
                        0x6aa17560, 0xf4210600, 0xd5023170, 0x3080f44f, 0xf44fe001, 0x43014080, 0xbd1062a1, 0x2300b530,
                        0x84836381, 0x84c32307, 0x8c83e010, 0x442388cc, 0x790b8483, 0x88cd8cc4, 0xd00107db, 0xe0002302,
                        0xfb052301, 0x31084303, 0x3a0884c3, 0xd2ec2a08, 0x1ccf3c3, 0xbd3084c1, 0xb1226b82, 0x8c82b109,
                        0x8cc0800a, 0xb1114770, 0xc126882, 0x6880800a, 0x47700cc0, 0x4604b510, 0x33cf100, 0xf7ff2100,
                        0x1ffeb, 0x6aa0d01f, 0x7080f440, 0x462062a0, 0xfe56f7ff, 0x201ea40, 0x43024817, 0x60424810,
                        0x7d02e002, 0x2b01f803, 0xf1a1000a, 0xb2890101, 0x2100d1f7, 0x42a33480, 0xf803d202, 0xe7fa1b01,
                        0x78969c1, 0xbd10d4fc, 0x22011c49, 0xf04f408a, 0x60826100, 0xd900428a, 0x60c2460a, 0x4770,
                        0x40003000, 0x20003, 0x38270, 0x419ce0, 0xa408300, 0x5204000, 0x72200000, 0x41f0e92d,
                        0x460d4604, 0x49fe69c0, 0x46984616, 0xd06e4288, 0x62a54620, 0xff6af7ff, 0xf1b068a0, 0xd9197f80,
                        0xf4406aa0, 0x62a07000, 0x28017c20, 0x2820d006, 0x28c2d00b, 0xf04fd009, 0xe6b81002, 0x22012380,
                        0x46202117, 0xfe1df7ff, 0x2200e004, 0x462021b7, 0xfdfef7ff, 0xd5040568, 0x680148ea, 0x5180f041,
                        0x4fe96001, 0xd5240768, 0x21352201, 0xf7ff4620, 0xb2c0fdef, 0x7817560, 0x7c0d455, 0x2201d135,
                        0x46202105, 0xfde4f7ff, 0xf0417d61, 0xea400102, 0xb2822001, 0x46202102, 0xfec8f7ff, 0xd1cc2800,
                        0x21352201, 0xf7ff4620, 0x7560fdd3, 0x7080ea4f, 0x4e8e019, 0x2201d51c, 0x46202105, 0xfdc8f7ff,
                        0x7520b2c0, 0xd42e0641, 0x240f040, 0x46202101, 0xfeacf7ff, 0xd1b02800, 0x21052201, 0xf7ff4620,
                        0x7520fdb7, 0x28000640, 0x4638db1d, 0xe04ee65f, 0xd5180728, 0x213f2201, 0xf7ff4620, 0xb2c0fda9,
                        0x6017560, 0xf040d40f, 0x22010380, 0x4620213e, 0xfdcef7ff, 0x213f2201, 0xf7ff4620, 0x7560fd99,
                        0x6000ea4f, 0x7a8e7df, 0x2200d505, 0x46202138, 0xfd8ef7ff, 0x6e8e017, 0x568d515, 0x2740d501,
                        0x2780e000, 0x21652201, 0xf7ff4620, 0xb2c0fd81, 0x42387560, 0xf040d007, 0x43bb03c8, 0x21612201,
                        0xf7ff4620, 0xf3c6fda5, 0x280340c1, 0xd0106aa0, 0x2080f420, 0x52862a0, 0xf3c6d507, 0x1e5b4302,
                        0x21c02201, 0xf7ff4620, 0xe9c4fd7c, 0x20006807, 0xf440e60d, 0xe7ed2080, 0x41f0e92d, 0x46044e99,
                        0x69b0460f, 0x46984615, 0xf40f410, 0x4601d04d, 0x40c1f3c0, 0x280361e1, 0x2000d04a, 0x462062a0,
                        0xfda9f7ff, 0x21ff2200, 0xf7ff4620, 0x2200fd41, 0x46112301, 0xf7ff2065, 0xf440fd28, 0xf7ff10c0,
                        0xf1a0fd0b, 0x29800140, 0x681d208, 0xf040d406, 0x220103c0, 0x46202161, 0xfd5af7ff, 0x46202180,
                        0xfcbff001, 0xc1f005, 0xd02428c1, 0x2170f44f, 0x4107ea01, 0x50c0ea41, 0x71fff64f, 0x60304408,
                        0x219f2203, 0xf7ff4620, 0xf04ffd13, 0x61204100, 0x1600e9c4, 0xf06fb130, 0x4288417f, 0x4973d002,
                        0xd10b4288, 0x1d404870, 0xf440e5b1, 0xe7af0140, 0x2080f44f, 0x486ce7b2, 0xe5a81e40, 0x4080f44f,
                        0x201c62a0, 0x209c8360, 0x4f658320, 0xd50107a8, 0xe0004638, 0xf8444866, 0x48660f1c, 0x20206060,
                        0x200c7620, 0x20d87520, 0x201076a0, 0xf81475a0, 0xf1a40c0c, 0x287f041c, 0xdc0cd029, 0xd01d281f,
                        0x2801dc04, 0x281cd014, 0xe014d139, 0xd0182820, 0xd1342837, 0x28c2e018, 0xdc04d022, 0xd019288c,
                        0xd12c28bf, 0x28c8e019, 0x28efd01d, 0xe01dd127, 0x447b4b51, 0x4b51e01c, 0xe019447b, 0x447b4b50,
                        0x4b50e016, 0xe013447b, 0x447b4b4f, 0x4b4fe010, 0xe00d447b, 0x447b4b4e, 0x4b4ee00a, 0xe007447b,
                        0x447b4b4d, 0x4b4de004, 0xe001447b, 0x447b4b4c, 0x4642b12b, 0x46204629, 0x46064798, 0x4e3ae001,
                        0xb3061d36, 0x61e72500, 0xf0014628, 0x2103fb1a, 0x22002301, 0xf7ff4608, 0x4601fc78, 0x46202200,
                        0xfc96f7ff, 0xb10d4601, 0xe00020ff, 0x42812000, 0x1c6dd102, 0xdbe72d02, 0xd10a2d02, 0xf4406aa0,
                        0x62a07000, 0x6aa0e005, 0xd5020400, 0xf7ff4620, 0x4620fe01, 0xfd73f7ff, 0xe5184630, 0x4dffe92d,
                        0x4683b08a, 0x90032000, 0x68c6980b, 0xf7ff4658, 0x4658fcc2, 0xfdaaf7ff, 0x8028f8db, 0x4048ea5f,
                        0xf8bbd576, 0xf0080018, 0xf4000104, 0x4308407f, 0x2001d000, 0x22014682, 0x46582105, 0xfc48f7ff,
                        0x14f88b, 0xaea5f, 0x2201d004, 0x46582135, 0xfc3ef7ff, 0x15f88b, 0x4014f8bb, 0xd0311c70,
                        0xf8bbb16e, 0xea240018, 0x40300200, 0xf10a4302, 0xb2c10001, 0xf7ff4658, 0x9003fd19, 0xe02ce067,
                        0x3803fff, 0x40003000, 0x20005, 0xcccccc, 0xb813fff, 0x2808000, 0x13e1, 0xe51,
                        0xc57, 0x1243, 0xbab, 0xd5d, 0xeef, 0x1461, 0x104f, 0xf99,
                        0x1529, 0x7800980c, 0x980db310, 0xf8bb8802, 0x4002001a, 0x43224384, 0xf8bbe7c9, 0x4220001a,
                        0x990cd037, 0x25002001, 0x980d7008, 0xf10a8004, 0xb2c70001, 0x1af8bb, 0xea244639, 0x46580200,
                        0xfcd4f7ff, 0xb1209003, 0x2d031c6d, 0xe189dbf2, 0x20a6e01f, 0xd1fd1e40, 0x21052201, 0xf7ff4658,
                        0xf88bfbd7, 0xea5f0014, 0xd004000a, 0x21352201, 0xf7ff4658, 0xf88bfbcd, 0xf8bb0015, 0xf8bb0014,
                        0x4208101a, 0x48f9d002, 0xe16b9003, 0x28009803, 0xf418d1dd, 0xd0da3f60, 0xf8db2000, 0x46045038,
                        0x20019006, 0xb10e9008, 0xe00020ff, 0x90092000, 0x90002000, 0xf44f980b, 0xe9d03780, 0x44081000,
                        0xf10b9002, 0x4682003c, 0xf8db9005, 0xa907001c, 0x5040f3c0, 0x90011cc0, 0xf7ff4658, 0x9004fd1d,
                        0xf8bdb915, 0x9006001c, 0x4008ea5f, 0xea5fd505, 0xd40250c8, 0xf7ff4658, 0x1c70fd1d, 0xb1b6d001,
                        0x980ce104, 0xb1587800, 0x4008ea5f, 0xe9ddd5f8, 0x990d2004, 0xfa9ef001, 0xf8ad2000, 0xe0f5001c,
                        0xf7ff4658, 0x2000fc7c, 0xe8bdb00e, 0x990c8df0, 0x70082000, 0x4008ea5f, 0xe9ddd5e2, 0x980d2104,
                        0xfa88f001, 0x9806e0e2, 0x88e8bb28, 0x68289006, 0xf9959000, 0x28000005, 0x4240da00, 0x40872701,
                        0x7c07928, 0x1b0d021, 0x1006ea40, 0x86ea40, 0xb2c04330, 0x20029009, 0x2c409008, 0x2c10d00c,
                        0x2c04d00a, 0x2c01d008, 0x2c20d006, 0x2c08d00a, 0x2c02d008, 0xe017d006, 0xf7ff4658, 0xf04ffc40,
                        0xe7c11002, 0x454ea44, 0xb10ee00e, 0xe00020ff, 0x90092000, 0x90082001, 0xd0032c30, 0xd0012c0c,
                        0xd1012c03, 0x444ea04, 0xb125b934, 0x7c07928, 0x24c0d001, 0x2480e000, 0x6801980b, 0x44389800,
                        0xd2784281, 0x98029900, 0xd9744288, 0x3f40f418, 0x1c70d063, 0x2e00d00b, 0xea5fdd1b, 0xd50b30c8,
                        0x2136460b, 0x9a014658, 0xfb32f7ff, 0xf89ae04e, 0x42200000, 0xe049d1f1, 0x22002301, 0x990120e5,
                        0xfae3f7ff, 0x23014601, 0x9a004658, 0xfb2ef7ff, 0xd13be03c, 0x30c8ea5f, 0x203cd501, 0x20e8e000,
                        0x22002301, 0xf7ff9901, 0x4601fad0, 0x9a004658, 0xfaeef7ff, 0xea5fb2c0, 0xd5023188, 0x78943c1,
                        0x7c0d00b, 0xea5fd025, 0xd50b30c8, 0x3200e9dd, 0x46582139, 0xfafcf7ff, 0x4658e010, 0xfbcff7ff,
                        0xe751487a, 0x22002301, 0x990120e5, 0xfaadf7ff, 0x23004601, 0x9a004658, 0xfaf8f7ff, 0x2001990c,
                        0xf89a7008, 0x43200000, 0xf88a, 0xbbe89803, 0xf89ae011, 0x43a00000, 0xf89ae7f6, 0x99092000,
                        0x4ea22, 0x43084021, 0xd0044282, 0xf88a, 0x2001990c, 0x98087008, 0xd10140c4, 0xa01f10a,
                        0xf995b135, 0x28000005, 0xf1c7da02, 0xe0000000, 0x99004638, 0x90004408, 0xf1a09806, 0x4000001,
                        0x90060c00, 0xb10dd102, 0x508f105, 0x1cf8bd, 0x101f1a0, 0x101cf8ad, 0xf47f2800, 0x980caf14,
                        0xb1187800, 0x4008ea5f, 0xe000d51c, 0x4658e01a, 0xfa9bf7ff, 0x99054658, 0xfa62f7ff, 0x43109a04,
                        0x43104a4b, 0x60504a4b, 0xf811e002, 0x75100b01, 0xf1a09804, 0xb29b0301, 0x28009304, 0x69d0d1f5,
                        0xd4fc0780, 0xf7ff4658, 0x9803fb5a, 0xb570e6dc, 0x6886680a, 0x6803b1ce, 0xd8064293, 0x684d68c4,
                        0x4415441c, 0xd30042ac, 0x42961ad2, 0x684bd910, 0x42b34413, 0x690cd80c, 0xf30f014, 0x68c0d002,
                        0xd8054283, 0x600a2000, 0x4830bd70, 0xbd701c80, 0x1e40482e, 0xb570bd70, 0x4615460c, 0xf7ff4606,
                        0x4630fa8a, 0xfa51f7ff, 0x608d492a, 0xf7ff4630, 0x6a32fa17, 0x260f402, 0x6204ea42, 0x60484310,
                        0xd0072cc7, 0xd0052c60, 0x46302101, 0x4070e8bd, 0xba91f7ff, 0xe7f82103, 0x460db570, 0x46044616,
                        0xfa33f7ff, 0x6085481b, 0x43316a21, 0xbd706041, 0x4df0e92d, 0x460e4683, 0x46984617, 0xf8df681c,
                        0x6855a054, 0x693be067, 0xb2d0683a, 0x7480f5c0, 0x42a5b113, 0x462cd200, 0xe0024621, 0x1e6d1c76,
                        0x7b01e64, 0x7830d009, 0xd11828ff, 0x2c00b1f5, 0xe01bd1f4, 0x1f2d1d36, 0x68301f24, 0xd10e1c40,
                        0xd30c2d04, 0xd2f52c04, 0xe00a, 0x20005, 0x42208000, 0x40003000, 0x1e6d1c76, 0xb12d1e64,
                        0x2c04b124, 0x7830d202, 0xd0f528ff, 0x44101b08, 0xb3956038, 0xd0c72c00, 0x46224601, 0xf7ff4658,
                        0x6838ffab, 0x60384420, 0x2c00e001, 0x4650d0bb, 0xd00b07b1, 0xb14cb1c5, 0x1b01f816, 0x1e6d7501,
                        0xe7f51e64, 0x6141ce02, 0x1f241f2d, 0xd3072d04, 0xd2f72c04, 0xf816e005, 0x75011b01, 0x1e641e6d,
                        0x2c00b115, 0xe000d1f7, 0x2102b92c, 0xf7ff4658, 0x2800fa12, 0x2d00d104, 0x2000d1d7, 0x4000f8c8,
                        0x6800e613, 0xe0044408, 0x1c496801, 0x1d00d104, 0x2a001f12, 0x2000d1f8, 0x68134770, 0x44186800,
                        0x40486010, 0xd0010780, 0x47702000, 0x47702001, 0x460cb53f, 0xaa02461d, 0xffeff7ff, 0xb948b335,
                        0x9802e022, 0x1b01f814, 0x42917802, 0x1c40d11f, 0x90021e6d, 0xd00b07a0, 0xd1f22d00, 0x9802e016,
                        0x68026821, 0xd1124291, 0x1d241d00, 0x90021f2d, 0xd2f42d04, 0x9802e008, 0x1b01f814, 0x42917802,
                        0x1c40d105, 0x90021e6d, 0xd1f42d00, 0xb0042000, 0xb5f8bd30, 0x6811460c, 0x68559100, 0x43de469c,
                        0x4621466a, 0xffb9f7ff, 0xf00cb385, 0xb1e803ff, 0x7a0b2f1, 0xb34dd018, 0xf8149f00, 0xf8170b01,
                        0x40582b01, 0x4210404a, 0xd11b9700, 0xe7f01e6d, 0x68209a00, 0xea806811, 0x4071000c, 0xd1114208,
                        0x1d241d12, 0x92001f2d, 0xd2f12d04, 0xb16db2f1, 0xf8149e00, 0xf8160b01, 0x40582b01, 0x4210404a,
                        0xd0019600, 0xbdf82001, 0xe7f01e6d, 0x2000e7ff, 0xe92dbdf8, 0x46174df7, 0x468bb09d, 0x46392214,
                        0xf001a802, 0x2500f85c, 0x5068f88d, 0x687ca902, 0xf7ff981d, 0x6fe9c, 0x9802d138, 0x4420901b,
                        0x46289018, 0x69389005, 0xd4070580, 0xaa1aab07, 0x981da902, 0xfc72f7ff, 0xd1270006, 0x981de0b1,
                        0xa01f04f, 0x1030f890, 0xf001fa0a, 0x1e429902, 0xeb004391, 0x91010801, 0xeba89902, 0x42ac0501,
                        0x4625d200, 0x69389503, 0xd4060740, 0xaa022300, 0x981d4659, 0xff7df7ff, 0x2001b100, 0x91199902,
                        0xd07d2800, 0x7006938, 0x48ead502, 0xe53cb020, 0xb30868b8, 0x1201e9dd, 0xa01eba2, 0x46429918,
                        0xd2034541, 0x9a184611, 0xe0001a89, 0x46882100, 0x10aea5f, 0x460ad005, 0xf0009901, 0x9801ffbb,
                        0xf1b89002, 0xd00a0f00, 0x464268b9, 0xaeb01, 0xf0009918, 0xe002ffaf, 0x800f04f, 0x981d46c2,
                        0xf8909a01, 0xf7ff1034, 0x6fe56, 0x981dd003, 0xf985f7ff, 0x6938e066, 0xd5100680, 0xf7ff981d,
                        0x981df97e, 0x99012201, 0x30f890, 0x981d4082, 0xfee7f7ff, 0xd1b92800, 0xf7ff981d, 0x2000f8cc,
                        0x90069000, 0xa00cf8cd, 0xaa02466b, 0x981d68b9, 0xfe5ef7ff, 0x95034606, 0xf00f1b8, 0x2000d003,
                        0xb1169006, 0x2001e008, 0x466be7fa, 0x4659aa02, 0xf7ff981d, 0x4606fe4d, 0xf8cd2001, 0x9006800c,
                        0x68b9b966, 0x4451466b, 0x981daa02, 0xfe40f7ff, 0xd1030006, 0xb1089800, 0x1602f04f, 0xe000981d,
                        0xf7ffe056, 0xb9eef93c, 0x6c06938, 0x462bd507, 0x9a194659, 0xf7ff981d, 0x6febb, 0x44abd112,
                        0x2c001b64, 0xaf4bf47f, 0xb15868f8, 0x981b9005, 0x68789002, 0xab079003, 0xa902aa1a, 0xf7ff981d,
                        0x4606fbad, 0xe7614630, 0xfff041, 0x1c6d1a45, 0xd20042ac, 0xf04f4625, 0xaa0233ff, 0x95034659,
                        0xf7ff981d, 0xb1f0fec6, 0xf7ff981d, 0x2000f864, 0x466b9000, 0x4659aa02, 0xa018f8cd, 0xf7ff981d,
                        0x4606fdf7, 0xf7ff981d, 0x2e00f8fa, 0x6938d1da, 0xd50b06c0, 0x4659462b, 0x981d9a19, 0xfe78f7ff,
                        0xd1cf0006, 0x9802e002, 0x90024428, 0x1b6444ab, 0xd0b92c00, 0x45419902, 0xaf01f4bf, 0xe92de7c4,
                        0xb09e4df3, 0x2214460c, 0xf000a802, 0x2600ff38, 0x606cf88d, 0x90016860, 0xf890981e, 0x20011030,
                        0x901a4088, 0x9618a902, 0xf7ff981e, 0x5fd70, 0x9605d17e, 0x5806920, 0xab07d407, 0xa902aa1b,
                        0xf7ff981e, 0x5fb4b, 0xe9ddd172, 0x44080101, 0x9000911c, 0xd16c2900, 0x6881981e, 0x42819801,
                        0x981ed867, 0x6406a80, 0x981ed463, 0xf803f7ff, 0x461a2300, 0x981e21c7, 0xffcaf7fe, 0x981e2103,
                        0xf819f7ff, 0x981e4605, 0xf899f7ff, 0x2703e09f, 0x4438981e, 0xf890901d, 0x28000030, 0x2101d07e,
                        0xf800fa01, 0xf1a89802, 0xea200101, 0xeba00b01, 0xeb0b060b, 0x90190008, 0x42819900, 0x1a40d201,
                        0x2000e000, 0x981a4682, 0xd2794286, 0xd2774582, 0xb16868a0, 0x4632b11e, 0xf0004659, 0xf1bafe8b,
                        0xd0050f00, 0x465268a0, 0x99004430, 0xfe82f000, 0x465a981e, 0xf8904438, 0x981e1034, 0xfd2bf7ff,
                        0x981e4605, 0xf85bf7ff, 0xd1702d00, 0x6806920, 0x981dd50a, 0x46592201, 0x30f890, 0x981e4082,
                        0xfdbff7ff, 0xd1030005, 0xb3c068a0, 0xe0012001, 0xe048e05e, 0xb1fe9006, 0xf7fe981e, 0xe9cdff9c,
                        0xab18b602, 0x68a1aa02, 0xf7ff981e, 0x4605fd31, 0xf7ff981e, 0xb925f834, 0xb1109818, 0x1502f04f,
                        0x6920e045, 0xd50606c0, 0x465a4633, 0x981e68a1, 0xfdaef7ff, 0xbbd54605, 0xf00f1ba, 0x981ed017,
                        0xff79f7fe, 0xe9cd9800, 0x68a00a02, 0x1981ab18, 0x981eaa02, 0xfd0cf7ff, 0xe0014605, 0xe006e010,
                        0xf7ff981e, 0xbb15f80c, 0x28009818, 0x9819d1d6, 0x98019002, 0xd90b4540, 0x8eba0, 0xe0029001,
                        0xf57f1e7f, 0x9801af65, 0xf47f2800, 0xb975af60, 0xb16068e0, 0x9002981c, 0x90036860, 0x900568e0,
                        0xaa1bab07, 0x981ea902, 0xfa78f7ff, 0x46284605, 0xe62c, 0x2000b, 0x41f0e92d, 0x7c847c46,
                        0x460f4605, 0xd0042e30, 0xd0072e40, 0xe8bd481c, 0xf1a481f0, 0x28070010, 0xe009d211, 0x15f1a4,
                        0xd20c2802, 0x401cf244, 0xf2448368, 0x832850fc, 0x46281e61, 0xf878f7ff, 0xd1052e40, 0x4810e002,
                        0xe7e41e40, 0xd50805f8, 0xf44f480e, 0x2c164188, 0x4b0dd301, 0x6a2be005, 0x480ce003, 0xf2444b0c,
                        0x2c160104, 0x2206d301, 0x2204e000, 0x5242ea40, 0x43024808, 0xe8bd4628, 0xf7ff41f0, 0xb86f,
                        0x20008, 0xbb010000, 0xa2888000, 0xeb030000, 0x32888000, 0x103fff, 0x41f0e92d, 0x7c404605,
                        0xf44f460f, 0x7ca94680, 0x343f1a0, 0xb24c3a, 0x800f04f, 0xd8252b05, 0xd140094b, 0x432f1a0,
                        0x28444616, 0x2845d006, 0x2846d00b, 0xf444d33d, 0xe03a7480, 0x22204931, 0x46284479, 0xffcef7fe,
                        0x2901e033, 0x492dd131, 0x44792220, 0x4628310e, 0xffc4f7fe, 0x219f2204, 0xf7fe4628, 0xe00fe59,
                        0xe022d1e5, 0xd0092865, 0xd0072866, 0xd0142886, 0xd0122887, 0x1c404820, 0x81f0e8bd, 0x456f1a0,
                        0xd0082865, 0x8368206c, 0x80f040, 0x20008328, 0x32f885, 0x2004e009, 0x949e7f5, 0x4620d001,
                        0x3872e7ea, 0x7440f440, 0x20524616, 0x35f885, 0xf885200f, 0xf2420031, 0x62e80005, 0x11ff004,
                        0xf7fe4628, 0xf414ffe1, 0xd0127f40, 0x7f40f5b4, 0x5f8d301, 0xf446d504, 0x4a096180, 0xe0034b09,
                        0x4b0a4a09, 0x108f046, 0xe8bd4628, 0xf7fe41f0, 0x4640bfe5, 0xe7bf62ae, 0x20007, 0xc54,
                        0x3b893fff, 0xa2888000, 0x6b893fff, 0x32888000, 0x4605b570, 0x7cac7c40, 0x289d460e, 0x482dd001,
                        0xf1a4bd70, 0x28010013, 0x380cd918, 0xd8032803, 0xf4443c11, 0xe0117480, 0xd0072c2f, 0x44f1a4,
                        0xd8062802, 0xf4443c31, 0xe0077440, 0x7487f44f, 0xf1a4e004, 0x2802007c, 0x3c6cd820, 0x11ff004,
                        0xd8022910, 0xf885200f, 0xf5b40032, 0xd3037f45, 0x8368203c, 0x832820bc, 0xf7fe4628, 0xf414ff85,
                        0xd0cd7040, 0x7040f44f, 0xd3014284, 0xd50d05f1, 0x4188f44f, 0xd9044284, 0xe0034a0f, 0x1e40480d,
                        0x4a0ebd70, 0x431a4b0e, 0xe0036a2b, 0x4b0e4a0d, 0x41a0f44f, 0xd9014284, 0xe0002006, 0xea422004,
                        0xf6435240, 0x430270ff, 0xe8bd4628, 0xf7fe4070, 0xbf75, 0x20008, 0xbb100000, 0x3b080000,
                        0x13fff, 0xeb133fff, 0x32888000, 0x41f0e92d, 0x7c867c45, 0x460f4604, 0xd0082d20, 0xbef005,
                        0xd0042830, 0xd0022d38, 0xe8bd4824, 0xf1a681f0, 0x28090010, 0x4821d302, 0xe7f61e40, 0xd8032e11,
                        0xf884200f, 0xe00c0032, 0xd10a2d20, 0xd1082e17, 0xf8042010, 0x20d80f30, 0x20007120, 0xf1a470a0,
                        0x1e710430, 0xf7fe4620, 0x2e16ff1f, 0x2d30d006, 0x2d70d002, 0xe005d002, 0xd3032e16, 0x8360203c,
                        0x832020bc, 0xbff005, 0xd0012830, 0xe7cc2000, 0x6a238b60, 0xc0f040, 0x5f88320, 0xf44fd503,
                        0x4a074188, 0x4a07e004, 0x102f244, 0x13c0f443, 0xe8bd4620, 0xf7fe41f0, 0xbf11, 0x20008,
                        0xbb913fff, 0xebdb3fff, 0x41f0e92d, 0x7c857c44, 0x460f4606, 0xd00a2c20, 0xd0082c21, 0xd0062c30,
                        0xd0042c40, 0xd0022c41, 0xe8bd4820, 0xf1a581f0, 0x28050013, 0x481dd302, 0xe7f61e40, 0xd0012c30,
                        0xd1052c41, 0x833020bc, 0xd1012c41, 0x8370203c, 0x46301e69, 0xfec8f7fe, 0xd5010660, 0xd50a05f8,
                        0x4188f44f, 0xd5010660, 0xe0004a11, 0x48124a11, 0x43026a33, 0x2d16e007, 0xf44fd009, 0x4a0f5080,
                        0xf4404b0f, 0xf0144180, 0xd0020f9f, 0x2004e005, 0x2d16e7f5, 0xf441d101, 0x6605100, 0xf442d501,
                        0x46300280, 0x41f0e8bd, 0xbeb8f7fe, 0x20008, 0xbb100000, 0x3b080000, 0x813fff, 0xeb933fff,
                        0x32888000, 0x41f0e92d, 0x6a064604, 0x7ca57c40, 0x2840460f, 0x4822d002, 0x81f0e8bd, 0x10f1a5,
                        0xd83a2807, 0xf8842052, 0x200f0035, 0x31f884, 0xd00b2d10, 0xd3052d14, 0xf88420d2, 0x20110037,
                        0x33f884, 0xd2052d16, 0xe005201c, 0xf8842000, 0xe7f90032, 0x1cf244, 0x2d168360, 0xf44fd202,
                        0xe00170fe, 0x50fcf244, 0x1e698320, 0xf7fe4620, 0x5f8fe5b, 0xf244d503, 0x4a0a4101, 0x4a0ae005,
                        0x105f244, 0xd3002d16, 0x48094e08, 0x43024633, 0xe8bd4620, 0xf7fe41f0, 0x4801be61, 0xe7bb1e40,
                        0x20008, 0xbb110000, 0xeb130000, 0x32888000, 0xc03fff, 0x4ff7e92d, 0x7c847c45, 0xf04f4606,
                        0xf44f0b00, 0x2d204a80, 0x2d24d008, 0x2d25d006, 0x2d5ed004, 0x485ad002, 0x8ffee8bd, 0x81ff004,
                        0x10f1a8, 0xd8722809, 0x101f1a8, 0xf7fe4630, 0x4954fe1b, 0xff004, 0x2c104479, 0x83705c08,
                        0x80f040, 0xd1028330, 0xf8862000, 0x22010032, 0x46302105, 0xfc4cf7fe, 0x7530b2c0, 0x740f010,
                        0xf040d119, 0xf0800040, 0x21010204, 0xf7fe4630, 0xea5ffd2d, 0xd1cf0b00, 0x21052201, 0xf7fe4630,
                        0xf080fc37, 0xb2c20004, 0xf0027532, 0x21010740, 0xf7fe4630, 0x2d20fd1b, 0x2d25d002, 0xe00fd004,
                        0xd3122c16, 0xe010b937, 0x33f1a4, 0xd9012806, 0xd30e2c53, 0xf8862052, 0x200f0035, 0x31f886,
                        0xd0022d20, 0xd0042d25, 0x2c17e01b, 0xb917d319, 0x2c34e034, 0xf1a8d315, 0x28060014, 0xe8dfd20f,
                        0x703f000, 0x26211c17, 0x22104927, 0xe0034479, 0x22104925, 0x31084479, 0xf7fe4630, 0xf04ffd5f,
                        0xb1cf0a80, 0xf4109801, 0xd1197f80, 0xe033e02b, 0x2210491d, 0x39084479, 0x491be7ee, 0x44792218,
                        0xe7e91e89, 0x22184918, 0x310c4479, 0x4916e7e4, 0x44792218, 0xe7df311a, 0xd11b2d20, 0xd3192c15,
                        0x2d20b137, 0x2c18d101, 0x20bbd902, 0xe0012102, 0x2101203b, 0xea400600, 0x480c42c1, 0x6180f44a,
                        0x6a334302, 0x4b0ae002, 0x46514a0a, 0xf7fe4630, 0x4683fd95, 0xe74f4658, 0x1e404801, 0xe74c,
                        0x20008, 0x8ec, 0x7c0, 0x813fff, 0x38908000, 0xebd33fff, 0x4602b50c, 0xe9d0a053,
                        0xe9cd3000, 0x5c83000, 0x2a4bd505, 0x2001d801, 0x2002bd0c, 0x2000bd0c, 0x5c0b4669, 0xd2024293,
                        0x28051c40, 0x1c40d3f9, 0xe92dbd0c, 0x46044df0, 0x468b4610, 0x7ca67c65, 0xffdef7ff, 0xf44fb2c7,
                        0xf04f4880, 0x2d200a0c, 0x2dbad00e, 0x2dbbd00c, 0x20dbd00a, 0x2d802108, 0x2d40d01a, 0x2d71d024,
                        0x483cd028, 0x8df0e8bd, 0xf88420d8, 0x2e110034, 0x200fd801, 0x2d20e006, 0x2e18d103, 0x2012d301,
                        0x2010e000, 0x30f884, 0xf8842000, 0xe0110032, 0x430f104, 0x70217120, 0x20f04f, 0xf8847160,
                        0xf1a4a001, 0xe0050430, 0x34f884, 0x1030f884, 0x840f04f, 0x10f1a6, 0xd302280a, 0x1e404825,
                        0x1e71e7d0, 0xf7fe4620, 0x2e13fcff, 0xf8a4d202, 0xe006a01a, 0xd3042dba, 0xd3042e17, 0x8360205c,
                        0x2d71e001, 0x2dbad011, 0x2dbbd00f, 0x2000d00d, 0xf0408b61, 0x43080080, 0x2d718320, 0xd106d322,
                        0x3111f44f, 0x4b154a14, 0x2020e017, 0x4814e7f0, 0xea5f62e0, 0xd50650cb, 0xf2444812, 0xea404130,
                        0x4b114207, 0x4811e005, 0xf2444b11, 0xea400130, 0x2e184207, 0xf441d301, 0x46203100, 0x4df0e8bd,
                        0xbcdcf7fe, 0xf8c42000, 0xe78b8028, 0x5f4e3b27, 0x6c, 0x20008, 0x3b893fff, 0xa2888000,
                        0x503070, 0xbbd83fff, 0xd2988000, 0xebd83fff, 0x12988000, 0x4604b510, 0x219f2205, 0xfae8f7fe,
                        0x28030e00, 0x4930d001, 0x493062e1, 0xb1197d09, 0xd0052901, 0xbd10482e, 0xf8842012, 0xe0030030,
                        0xd1012803, 0x8360203c, 0x46207ca1, 0xf7fe1e49, 0x2000fc8b, 0xb570bd10, 0x460d4604, 0x7ca17c40,
                        0xf88422d8, 0x22102034, 0x2030f884, 0xf8842200, 0x4a1f2032, 0x28021c52, 0x2820d003, 0x1c50d013,
                        0xf1a1bd70, 0x28020012, 0x4620d803, 0xfc6cf7fe, 0xf1a1e013, 0x28010015, 0x4813d802, 0xe7f462e0,
                        0xd0042919, 0x2918e001, 0x4610d001, 0x4620bd70, 0xffb0f7ff, 0xfff010, 0x6ae0d1f8, 0xd0f52800,
                        0xf4408b60, 0x83205036, 0xd50405e8, 0x4188f44f, 0x6a234a08, 0x4a08e003, 0xf2444b08, 0x46200104,
                        0x4070e8bd, 0xbc5af7fe, 0x306005, 0x40003000, 0x20006, 0xbbd13fff, 0xebd33fff, 0x32888000,
                        0x4604b570, 0x7c807c41, 0x29264a26, 0x2925d003, 0x1c50d02d, 0xf000bd70, 0x290301df, 0x2107d829,
                        0x210074e1, 0x507f000, 0x1032f884, 0x113f105, 0xf7fe4620, 0x2d01fc19, 0x2d02d004, 0x2d03d006,
                        0xe00fd10b, 0x22284918, 0xe0034479, 0x22284916, 0x31204479, 0xf7fe4620, 0x4b14fbb1, 0xf2484a14,
                        0xe01a0102, 0x22284910, 0x31304479, 0x284be7f2, 0x4610d001, 0x2116bd70, 0xf7fe4620, 0x203cfbf5,
                        0x20bc8360, 0x20528320, 0x35f884, 0x4b09200f, 0xf8844a09, 0xf44f0031, 0x462041c8, 0x4070e8bd,
                        0xbbfcf7fe, 0x20007, 0x4e8, 0x2988000, 0xb993fff, 0xa2888000, 0xbb913fff, 0x4602b508,
                        0x4669a039, 0x90006800, 0x5c0b2000, 0xd2024293, 0x28031c40, 0x1c40d3f9, 0xe92dbd08, 0x469041f0,
                        0x460b7c47, 0x4a317c86, 0xf44f4604, 0xf44f4580, 0x2f304188, 0xf017d003, 0xd0090f8f, 0xf1a6e029,
                        0x28040010, 0x8b20d20a, 0x20f040, 0xe0108320, 0xd01e2f70, 0x12f1a6, 0xd3022808, 0xe8bd4610,
                        0xf24481f0, 0x8360001c, 0x10fcf244, 0x5d88320, 0x460dd500, 0x46201e71, 0xfb96f7fe, 0xf8842052,
                        0x200f0035, 0x31f884, 0xd5050568, 0x6a234a18, 0x4816e011, 0xe7e21c40, 0xd00f2f60, 0x21022203,
                        0x504f244, 0x4122001, 0x42c1ea42, 0x430a4911, 0xea414911, 0x2f4043c0, 0xe00ed009, 0x504f644,
                        0xf7ff4640, 0xb2c2ff9b, 0x46012003, 0x2e14e7eb, 0x2e16d303, 0xf045d801, 0x46290501, 0xe8bd4620,
                        0xf7fe41f0, 0xbb7b, 0x50321e, 0x20007, 0xbbd13fff, 0xebc03fff, 0x32808000, 0x49514a52,
                        0x4a526011, 0x112f04f, 0xf1026011, 0xf04f0204, 0x60110142, 0xf04f494e, 0xfb000280, 0xf44ff001,
                        0xfbb011e1, 0x484bf1f1, 0xb2ca60c2, 0xea4f6002, 0x60412111, 0x107f04f, 0xf04f60c1, 0x60810147,
                        0xb1284770, 0xd0052801, 0x494320d3, 0x47706008, 0xe7fa20db, 0xe7f820c3, 0x20f34940, 0xf04f6008,
                        0x610800d3, 0x608860c8, 0xf04f6048, 0x61480013, 0xb5f04770, 0x4c34460f, 0x3ca02100, 0x4b3861a1,
                        0x6163e005, 0x2116962, 0xf3c2d4fc, 0x3978214d, 0xd2f62929, 0xd90128a0, 0xe00220a0, 0xd200280a,
                        0xf44f200a, 0xfbb171a0, 0x4358f3f0, 0xfbb0210c, 0x4a2cf0f1, 0xea421e41, 0x6c624501, 0x40164e2a,
                        0xd01342ae, 0xf3c66ee6, 0x2e0c6604, 0x4e27d101, 0x7d666e6, 0xf042d106, 0x64620201, 0x1c522200,
                        0xd9fc2aff, 0x6c216465, 0xd0fc07c9, 0x140eb00, 0x7296f44f, 0xf81ebb2, 0x2103d201, 0x2296e006,
                        0xf81ebb2, 0x2102d201, 0x2101e000, 0x1f12008a, 0x6210f042, 0x9a64a2, 0xf0421f12, 0x65a26210,
                        0x66e24a08, 0x67224a12, 0x40eb00, 0xfbb50085, 0x4620f4f1, 0xff62f7ff, 0x603cb107, 0xf0f3fbb5,
                        0xbdf0, 0xc000800, 0x400500a0, 0x40086634, 0xf4240, 0x40082000, 0x40086198, 0x4008618c,
                        0x6800078, 0x6000080, 0xfff33c3, 0x1000800, 0x10000800, 0xf2402a03, 0xf0108030, 0xf0000c03,
                        0xf8118015, 0xf1bc3b01, 0x44620f02, 0xf811bf98, 0xf800cb01, 0xbf383b01, 0x3b01f811, 0x204f1a2,
                        0xf800bf98, 0xbf38cb01, 0x3b01f800, 0x303f011, 0x8025f000, 0xf0c03a08, 0xf8518008, 0x3a083b04,
                        0xcb04f851, 0x1008e8a0, 0x1d12e7f5, 0xf851bf5c, 0xf8403b04, 0xf3af3b04, 0x7d28000, 0xf811bf24,
                        0xf8113b01, 0xbf48cb01, 0x2b01f811, 0xf800bf24, 0xf8003b01, 0xbf48cb01, 0x2b01f800, 0xb5104770,
                        0xf0c03a20, 0xe8b1800b, 0x3a205018, 0x5018e8a0, 0x5018e8b1, 0x5018e8a0, 0xaff5f4bf, 0x7c02ea5f,
                        0xe8b1bf24, 0xe8a05018, 0xbf445018, 0xc018c918, 0x4010e8bd, 0x7c82ea5f, 0xf851bf24, 0xf8403b04,
                        0xbf083b04, 0x7d24770, 0xf831bf28, 0xbf483b02, 0x2b01f811, 0xf820bf28, 0xbf483b02, 0x2b01f800,
                        0xf04f4770, 0xb5000200, 0x46944613, 0x39204696, 0xe8a0bf22, 0xe8a0500c, 0xf1b1500c, 0xf4bf0120,
                        0x709aff7, 0xe8a0bf28, 0xbf48500c, 0xf85dc00c, 0x89eb04, 0xf840bf28, 0xbf082b04, 0xbf484770,
                        0x2b02f820, 0x4f80f011, 0xf800bf18, 0x47702b01, 0x0, 0x71000, 0x70000, 0x10f00,
                        0x78000, 0x20d00, 0x7c000, 0x10e00, 0x0, 0xf1000, 0xf0000, 0x10e00,
                        0xf4000, 0x20d00, 0xf8000, 0x10f00, 0x0, 0x100c00, 0x10000, 0xf1000,
                        0x0, 0x100c00, 0x10000, 0x1f1000, 0x0, 0x100c00, 0x10000, 0x3f1000,
                        0x0, 0x100c00, 0x10000, 0x7e1000, 0x7f000, 0x100c00, 0x0, 0x100c00,
                        0x10000, 0xfe1000, 0xff000, 0x100c00, 0x0, 0x100c00, 0x10000, 0x1fe1000,
                        0x1ff000, 0x100c00, 0x3c7c0c0c, 0x3c3c3c3c, 0x3c3c, 0x1fe000, 0x4f301, 0x6000,
                        0x4f301, 0x1f0000, 0x1f100, 0x8000, 0x1f100, 0x1e0000, 0x1ef000, 0x3fe000,
                        0x4f301, 0x6000, 0x4f301, 0x3f0000, 0x1f100, 0x8000, 0x1f100, 0x3e0000,
                        0x3ef000, 0x7fe000, 0x4f301, 0x6000, 0x4f301, 0x7f0000, 0x1f100, 0x8000,
                        0x1f100, 0x7e0000, 0x7ef000, 0x0,
                        0x00000000,
                        0x06802005, # movs r0, #5      ; Call pc_init routine with r0 forced to start of FLASH.
                                    # lsls r0, r0, #26 ; start of FLASH = 5 << 26 = 0x14000000
                        0xbef6f7fd, # b 0x10000028
                        0x00000000
                                ],
               'pc_init'         : 0x10002234, # Call through thunk added to force r0 to 0x14000000
               'pc_eraseAll'     : 0x1000007F,
               'pc_erase_sector' : 0x1000009F,
               'pc_program_page' : 0x100000CD,
               'begin_data'      : 0x10004000,  # Analyzer uses a max of 128 KB data (32,768 pages * 4 bytes / page)
               'page_buffers'    : [0x10004000, 0x10004800],   # Enable double buffering
               'begin_stack'     : 0x10008000,
               'static_base'     : 0x10002240,
               'min_program_length' : 512,
               'analyzer_supported' : False,    # Analyzer works, but would fail if a full ROM analysis was performed since there is not enough ram
               'analyzer_address' : 0x10005000  # Analyzer 0x10005000..0x10005600
              }

class LPC4330(CoreSightTarget):

    VENDOR = "NXP"
    
    memoryMap = MemoryMap(
        FlashRegion(    start=0x14000000,  length=0x4000000,    blocksize=0x400, is_boot_memory=True,
            algo=FLASH_ALGO),
        RamRegion(      start=0x10000000,  length=0x20000),
        RamRegion(      start=0x10080000,  length=0x12000),
        RamRegion(      start=0x20000000,  length=0x8000),
        RamRegion(      start=0x20008000,  length=0x8000)
        )

    def __init__(self, link):
        super(LPC4330, self).__init__(link, self.memoryMap)
        self.ignoreReset = False
        self._svd_location = SVDFile.from_builtin("LPC43xx_svd_v5.svd")

    def reset(self, reset_type=None):
        # Always use software reset for LPC4330 since the hardware version
        # will reset the DAP.
        super(LPC4330, self).reset(self.ResetType.SW)

    def reset_and_halt(self, reset_type=None):
        if self.ignoreReset:
            return

        # Set core up to run some code in RAM that is guaranteed to be valid
        # since FLASH could be corrupted and that is what user is trying to fix.
        self.write_memory(0x10000000, 0x10087ff0)    # Initial SP
        self.write_memory(0x10000004, 0x1000000d)    # Reset Handler
        self.write_memory(0x10000008, 0x1000000d)    # Hard Fault Handler
        self.write_memory(0x1000000c, 0xe7fee7fe)    # Infinite loop
        self.write_memory(0x40043100, 0x10000000)    # Shadow 0x0 to RAM

        # Always use software reset for LPC4330 since the hardware version
        # will reset the DAP.
        super(LPC4330, self).reset_and_halt(self.ResetType.SW)

        # Map shadow memory to SPIFI FLASH
        self.write_memory(0x40043100, 0x80000000)

        # The LPC4330 flash init routine can be used to remount FLASH.
        self.ignoreReset = True
        self.flash.init(Flash.Operation.VERIFY)
        self.ignoreReset = False

        # Set SP and PC based on interrupt vector in SPIFI_FLASH
        sp = self.read_memory(0x14000000)
        pc = self.read_memory(0x14000004)
        self.write_core_register('sp', sp)
        self.write_core_register('pc', pc)
