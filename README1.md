# 项目二文件结构

```
|-- Python 项目二
	|-- Unit 网元
		local->tuple
		dest->tuple
		|--start()
		|--send()
		|--receive()
		|-- tcpLayer网络层
			|--controlCenter()
			|--recvFrame()->list:frame
			|--sendFrame(str:text)->void
			|--checkXor(list:Frame)->bool:res
		|-- dataLayer 数据链路层
			|-- wrapChunk(rawFrames)->list:Frames
			|-- parseChunk(recvFrames)->list:checkedFrames
	|-- method 方法
		|--Oddcheck(list:Frames)->list:result[[row],[crowd]]
		|--bytes2Bin(bytestr:bytes)->str:rawBin
		|--bin2Frames(str:bindata)->list:Frame
		|--frames2Bin(list:Frames)->str:rawBin
		|--bin2Bytes(str:rawBin)->bytes:bytes
		|--text2Bytes(str:bytes)->str:bytes
		|--addXorCheck(list:Frame)->str:text
```

## 设计

按帧传输一帧8\*8 bit + 2\*8校验位 = 80bit，二维奇偶校验

或者是采用16\*16+2*16 = 288bit，由于UTF-8编码问题有ASCII字符是8bit，所以就可能会出现只有8bit而不是16bit，就采用在最后面加入8个0的方式进行区分

层与层之间直接采用List的方式传帧，[[],[],[]]的方式

数据链路层：

text->text2Bytes()->bytes2Bin()->bin2Frames()->Frame->oddcheck->bin->bytes->send

recv->bin->Frame->oddcheck()->checkXor()->Frame2bin()->bin2bytes()->bytes2text()

网络层：

sender: send->recv->send

recver : recv->send : ack->recv()

**建议**

每个函数单独写出来，自己构造数据检查完备之后再粘贴进去

---



## 发送过程

根据误码率20/100000，传输5000个错1个，所以按照288为一帧太不划算，而且帧这个应该是在网络层包装，网络层中的极限数据bit位是4000个，我们就取3200个,也就是400字节（测试用例根本取不到）

'10110111'-->8bit为1字节

### 网络层

数据`hello world!你好啊嘤嘤嘤`

#### ----转化为bytes流---->

`b'hello world!\xe4\xbd\xa0\xe5\xa5\xbd\xe5\x95\x8a\xe5\x98\xa4\xe5\x98\xa4\xe5\x98\xa4'`

#### ----转化为2进制字符串---->

'101010101010101010101010101......10101010'

#### ----按照8bit来分成字节，然后过长则分帧---->

[['11111111','11111111','11111111',......(最多386个字节单元)......,'11111111'],

['11111111','11111111','11111111',......(最多386个字节单元)......,'11111111'],

['11111111','11111111','11111111',......(最多386个字节单元)......,'11111111'],

........

['11111111','11111111','11111111',......(最多386个字节单元)......,'11111111']]

#### ----一次性发送16个帧---->

循环开始->16次

#### ----选取一个帧添加头尾部---->

帧编号:`00-0f`,1字节

源IP:`ff.ff.ff.ff`,4字节，源端口:`ffff`，2字节

目的IP:`ff.ff.ff.ff`，4字节，目的端口:`ffff`,2字节

尾部：所有字节全部XOR一次，结果1字节

头部尾部算上一共要添加14字节

#### ----发送一个帧到数据链路层---->

循环结束->16次

#### ----进入接收信号模式---->

----

### 数据链路层

['11111111','11111111','11111111',......,'11111111']

#### ----分校验单元---->

[['11111111','11111111'....(8个字节)......'11111111'],

['11111111','11111111'....(8个字节)......'11111111'],

............

['11111111','11111111'....(8个字节)......]]

其中[[],[],[],[]]为一个帧，里面的['111111','10101010',...（8个bit）...,'11100011']称为一个**校验单元**

#### ----二维奇偶校验---->

[['11111111','10101010'....(10个字节，8字节数据，2字节校验)........'11111111'],

['11111111','10101010'....(10个字节，8字节数据，2字节校验)........'11111111'],

['11111111','10101010'....(10个字节，8字节数据，2字节校验)........'11111111'],

['11111111','10101010'....(10个字节，8字节数据，2字节校验)........'11111111']]

#### ----转化为bytes流---->

`\xef\xab\x0c\xc0......\xab\x3a`

#### ----前后加上`\xee\xff`作为帧开始符，加上`\xff\xee`作为结束符---->

`\xee\xff\xef\xab\x0c\xc0......\xab\x3a\xff\xee`

#### ----发送---->

---

## 接收过程

### 数据链路层

#### ---- 接收bytes流---->

`\xee\xff\xef\xab\x0c\xc0......\xab\x3a\xff\xee`

#### ----按照`\xee\xff`开始`\xff\xee`作为帧定位符提取---->

`\xef\xab\x0c\xc0......\xab\x3a`

#### ----判断是否为结束符`\xff\xee\xdd\xff\xff\xdd\xee\xff`---->

#### ----转化为01流---->

'11111111000000000101010110101010......'

#### ----按照8个字节为一个校验单位进行分帧处理---->

[['11111111','10101010'....(10个字节，8字节数据，2字节校验)........'11111111'],

['11111111','10101010'....(10个字节，8字节数据，2字节校验)........'11111111'],

['11111111','10101010'....(10个字节，8字节数据，2字节校验)........'11111111'],

['11111111','10101010'....(10个字节，8字节数据，2字节校验)........'11111111']]

#### ----二维奇偶校验校错，去掉校验位---->

[['11111111','11111111'....(8个字节)......'11111111'],

['11111111','11111111'....(8个字节)......'11111111'],

............

['11111111','11111111'....(8个字节)......]]

#### ----校验单位合并成为一个帧---->

['11111111','11111111','11111111',......,'11111111']

#### ----网络层---->

### 网络层

['11111111','11111111','11111111',........(最多400字节)........,'11111111']

#### ----提取并去掉帧头尾信息---->如果xor校验有误，break，并发送RR+帧序号

['11111111','11111111','11111111',......(最多386字节)........,'11111111']

#### ----转化为二进制字符串---->

'111111110101010101........010101010'

#### ----转化为bytes流,并缓存---->

`\xee\xff\xef\xab\x0c\xc0......\xab\x3a\xff\xee`

#### ----接收到了结束符之后---->

#### ----所有bytes流解码成为数据---->

`hello world!你好啊嘤嘤嘤......`

---

## 流量控制

### 服务端

----发送8个帧---->接收状态信号---->决定重传8帧的起点或者是n---->循环

客户端

----开始接受一个帧（有很短的超时限制）---->检验是否为坏帧---->发送`ACK n` 或者是`ARQ n` 

---

**物理层UDP模拟软件限制，无法使用TCP模式连接，只能用UDP来模拟TCP**