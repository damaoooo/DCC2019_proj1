# 项目一总报告

[toc]

## 一、主题

​	设计具有多层结构的网元，并将多个网元构成一个网络，实现信息、文件在多个网元之间的传递。

## 二、目标

​	利用项目提供的物理层模拟软件，在两个只能传输0和1数据的程序（物理层实体的仿真）之间通过增加各种控制功能，形成多层结构网元，网元之间形成多种拓扑结构，通过网元传输包含中文、英文、标点符号（大约50个字符）和图片文件等，并编程实现。

## 三、总览

### 3.1 分工情况

#### 3.1.1  周立（40%）

* 规划项目设计
* 编写主要代码
* 完成代码框架设计
* 管理合作平台`github`的项目

#### 3.1.2 李学良（30%）

* 竞争式实验项目
* 参与讨论项目
* 实验报告和PPT准备

#### 3.1.3 朱星昶（30%）

* 参与讨论项目
* 代码调试debug
* 实验报告和PPT准备

### 3.2、亮点

* 基于滑动窗口的流量控制协议
* 能够传输中文英文日文等多种文字，以及传输图片和文件
* 具有纠错能力和校错重传能力
* 基于RIP协议的动态路由
* python的面向对象编程
* 结构化，API抽象的编程，提高可读性
* 使用XOR校验代替CRC校验
* 编写一键启动代码减小工作量
* 通过`GitHub`的在线合作方式
* 具有`CLI`的过程展示，错误原因以及传输过程

### 3.3 任务阶段

#### 3.3.1 阶段一  socket初体验，熟悉代码

​	熟悉套接字编程，编写小程序作为试验

​	熟悉了socket和select函数居然还有这种功能，由于python的简便性与通用性，我们在这一阶段确定了我们的编程语言使用python

#### 3.3.2 阶段二  小试牛刀，搭建底层

​	完成帧同步，差错控制，流量控制

​	这是我们花费时间最多的一个阶段，我们不仅想要能够发现错误，还想要对错误进行检测并改正，减少重传的次数，因此我们使用了二维奇偶校验的方式。如果运气实在不好除了很多错必须重传的检验，我们抛弃了CRC校验，收到了密码学的影响，我们设计了XOR校验的形式

​	尽管重传率被我们控制得非常低，但是我们不满足于停等协议，选择了滑动窗口的设计，提高了传输的效率，这直接导致了我们将代码重构了好几次，也为后面的路由设计添加了很多麻烦，但是这是最贴合实际的，也是我们应该下功夫去研究的地方

#### 3.3.3 阶段三  完成交换机的配置

​	完成交换接口排队模型这几——多接入的寻址设计

​	这里我们对物理层模拟软件进行了研究，同时也发现了之前滑动窗口协议的不足，对之前的代码进行了重构。受益于之前基于API的结构化编程，我们的交换机代码部分非常少，就实现了交换机的转发功能

​	但是在转发的时候经常发现程序会各种死掉，这让我们非常痛苦，因此我们进行了数十次debug修复。

#### 3.3.4 阶段四  大展拳脚，完成路由器的配置

​	三层到二层的寻址技术，完成路由及转发，完成动态路由

​	在这里我们自己设计了一个网络拓补结构，没有像之前一样一上来就写，我们在这里先规划好了端口号和路由表的过程，然后根据函数内容选择了多文件编程，最后逐一进行配置和测试。我们发现需要启动十多个物理层模拟软件比较麻烦，于是我们编写了一键启动的代码，省时省力

​	最后我们还发现了一个异常，在发包速率过快的时候，软件有几率会进入一个自己给自己发包然后接收的死循环，因此我们编写了一个帧过滤程序，过滤掉重复的包，使软件恢复正常，解决了这个问题，我们还试着传输了图片和多种文字。

## 四、实验过程

### 4.0  环境介绍

#### 4.0.1 编写及运行环境

*  python 3.7.0

* Microsoft Windows 10 pro x64

* Microsoft Visual Studio Code

#### 4.0.2 合作环境

* GitHub

![image-20191221203622226](assets/image-20191221203622226.png)

* QQ群

![TIM图片20191221203823](assets/TIM图片20191221203823.png)

* `hackmd`合作文档

![image-20191221203718742](assets/image-20191221203718742.png)

### 4.1 数据链路层

#### 4.1.0 项目初步设计

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

​	后来我们发现这种提前设计非常方便，能够帮助我们理清编程逻辑，剩下的就是分模块编写代码然后测通即可，非常有益处，这是最初的一份设计表，到后面由于功能的增加，我们基于这份表格添加了函数和功能

#### 4.1.1 基于比特流的帧定位

​	由于物理信道中存在干扰和噪声，而且我们的数据的开始和结束往往之间并不是空白，这一点物理层模拟软件也模拟了出来,例如

输入为
$$
input = 11100010
$$


经过了物理信道之后的输出为
$$
output = 1101010101001111000101010011010
$$
​	其中我们原来的输入`11100010`就在接收到的一串比特流之间，因此我们需要将其提取出来，就需要帧定位的定位符。我们在设计定位符的时候有如下考虑：

1. 不能太短，如果噪声中也有这个定位符就会导致帧定位失败

2. 不能够在要传输的字符里面出现，否则会定位失败

3. 要能够避免比特重合的情况，如定位符是`1111`，结果收到的数据含有`11111`，就无法确定哪一位是帧开头的一位

   最后我们选择了`\xee\xff`作为帧定位符的开始符，`\xff\xee`作为帧定位符的结束符

实现的代码如下

```python
    def direction(self,text,keystart,keyend):
        start = text.find(keystart)
        end = text.find(keyend)
        if(start!=-1 and end!=-1):
            return text[start+len(keystart):end]
        else:
            return -1
```

​	如果定位正常，就返回定位后的比特流，如果定位失败，返回`-1`作为异常。

#### 4.1.2 二维奇偶校验纠错

​	纠错目前的方法是海明编码，增加汉明距离，奇偶校验，二维奇偶校验等方法，我们逐一比较了每个方法。

​	**奇偶校验：**

​	（以下指奇校验），对编码的1的个数计数，如果是奇数个，那么在码的后面添加一个1，反之添加一个0

​	例如`10110`，里面有3个`1`，奇数个，那么在后面添加一个`1`，编码为`101101`

​	例如`10100`，里面有2个`1`，偶数个，那么在后面添加一个`0`，编码为`101000`

​	如果全部使用奇偶校验的话，只能够校验出1个错误，如果是偶数个错误就完了，这是我们不想要看到的，而且奇偶校验只能够发现错误，并不能够对错误进行定位，显然不符合我们的需要

​	**海明编码：**

​	用数学术语来说，汉明码是一种二元线性码。对于所有整数 *r* ≥ 2，存在一个分组长度 *n* = 2*r* − 1、*k* = 2*r* − *r* − 1 编码。因此汉明码的码率为 *R* = *k* / *n* = 1 − *r* / (2*r* − 1)，对于最小距离为3、分组长度为 2*r* − 1 的码来说是最高的。汉明码的奇偶检验矩阵的是通过列出所有长度为 *r* 的非零列向量构成的。

​	由于海明编码过于复杂，在涉及到比较大的数据传输的时候会出现数据位和校验位夹杂的现象，不利于我们进行数据的提取，我们放弃了这种方法

​	**二维奇偶校验：**

​	这是我们采用的方法，二维校验是一个矩阵，在一个矩阵内任意一个比特除了错误我们都有矫正的能力，而矩阵的大小我们也是考虑之后有8，16两种选择，由于我们的数据是采用的`UTF-8`编码，`ASCII`码是`8bit`表示一个字符，因此如果是长度是16，就会有数据浪费的情况

​	我们将数据按照8bit为一个字节，8个字节为一组的方式进行二位奇偶校验，原理如下图

<img src="assets/image-20191221014147604.png" alt="image-20191221014147604" style="zoom: 50%;" />

​	一旦某一位发生了错误，那么就会反应在相应的`x`和`y`坐标中，这样就可以针对这一位进行纠错，如果出现在不同行不同列的两个错误，也可以进行纠正。

生成校验位的代码如下

```python
def oddCheck(self,checkUnit):
        rowRes = [0]*8
        colunmRes = [0]*8
        for singleByteIndex in range(len(checkUnit)):
            #row:行  colunm:列
            listBytes = list(checkUnit[singleByteIndex])
            for singleBitIndex in range(len(listBytes)):
                num = int(listBytes[singleBitIndex])
                rowRes[singleByteIndex]^=num
                colunmRes[singleBitIndex]^=num
        return [''.join([str(x) for x in rowRes]),''.join([str(y) for y in colunmRes])]     
```

进行校错的代码如下

```python
    def findDiffrent(self,bytes1,bytes2):
        res = []
        for i in range(len(bytes1)):
            if(bytes1[i]!=bytes2[i]):
                res.append(i)
        return res    
    def parseChunk(self,oneFrame):
            chunks = []
            while(oneFrame!=[]):
                oneChunk = oneFrame[0:10]
                chunks.append(oneChunk)
                oneFrame = oneFrame[10:]
            for chunkIndex in range(len(chunks)):
                oddCheckRecv = chunks[chunkIndex][-2:]
                data = chunks[chunkIndex][:-2]
                selfCheck = self.oddCheck(data)
                if(selfCheck == oddCheckRecv):
                    chunks[chunkIndex]=data
                    continue
                else:
                    diff = [self.findDiffrent(oddCheckRecv[0],selfCheck[0]),self.findDiffrent(oddCheckRecv[1],selfCheck[1])]
                    x,y = diff[0],diff[1]
                    if(len(x)+len(y)==1):
                        chunks[chunkIndex] = data
                        continue
                    elif(len(x)==len(y)):
                        for i in range(len(x)):
                            try:
                                errorData = list(data[x[i]])
                            except:
                                print('found ERR!->',data)
                            errorData[y[i]] = str(int(errorData[y[i]])^1)
                            patchData = ''.join(errorData)
                            data[x[i]]=patchData
                chunks[chunkIndex] = data
            res = []
            for i in chunks:
                res +=i
            return res
```

进行包装的时候每8个字节进行一个打包，然后生成2个字节的校验位在后面，一个`chunk`就是10个字节

进行解包的时候每10个字节进行一个分组，将前8个字节进行奇偶校验生成两个字节的校验位，同接收到的校验位进行对比，然后进行查验和恢复

#### 4.1.3 使用XOR进行帧校验

​	采用XOR校验方式源自于之前深夜做题的一次经历

​	二战期间，各国为了电报加密，对密码学进行了大量的研究和实践，其中就包括 XOR 加密。战后，美国数学家香农`Claude Shannon`将他的研究成果公开发表，证明了只要满足两个条件，XOR 加密是无法破解的：

- `key`的长度大于等于`message`。
- `key`必须是一次性的，且每次都要随机产生。

​	CRC32同XOR校验具有一样的功能，即便`python`中有现成的库，但是CRC32校验在这里太麻烦了，因此我们自己设计了一个XOR校验

​	我们这里采用的是对帧的所有字节进行一次`XOR`操作，生成一个校验码，加在帧的最后面，只要帧有1位经过前面的二位奇偶校验还是不能纠错，那么这个校验码就会不一样，就可以确定需要重传了

代码如下

```python
    def addXorCheck(self,Frame):
        sumxor = 0
        for onebyte in Frame:
            sumxor ^=eval('0b'+onebyte)
        return bin(sumxor)[2:].zfill(8)
```

​	在接收到帧的时候计算帧的校验码，同原来接收到的校验码进行比对即可

#### 4.1.4 流程说明

​	接收到一个比特流，数据链路层的流程如下

**----接收比特流---->**

`'101010101010101010101010101......10101010'`

**----帧定位---->**

`'101010101010101010101010101......10101010'`

**----按照8bit来分成字节,一帧有400bit---->**

```
[['11111111','11111111','11111111',......(最多400个字节单元)......,'11111111'],

['11111111','11111111','11111111',......(最多400个字节单元)......,'11111111'],

['11111111','11111111','11111111',......(最多400个字节单元)......,'11111111'],

........

['11111111','11111111','11111111',......(最多400个字节单元)......,'11111111']]
```

**----进行奇偶校验分chunk---->**

```
[['11111111','10101010'....(10个字节，8字节数据，2字节校验)........'11111111'],

['11111111','10101010'....(10个字节，8字节数据，2字节校验)........'11111111'],

['11111111','10101010'....(10个字节，8字节数据，2字节校验)........'11111111'],

['11111111','10101010'....(10个字节，8字节数据，2字节校验)........'11111111']]
```

**----二维奇偶校验纠错，去掉校验位---->**

~~~
[['11111111','11111111'....(8个字节)......'11111111'],

['11111111','11111111'....(8个字节)......'11111111'],

............

['11111111','11111111'....(8个字节)......]]
~~~

**----计算XOR校验，决定是否重传---->**

### 4.2 成帧设计

#### 4.2.1 帧结构说明

| 发送者IP | 发送者端口 | 接收者IP | 接收者端口 | 帧序号 |  数据   | XOR校验位 |
| :------: | :--------: | :------: | :--------: | :----: | :-----: | :-------: |
|  4字节   |   4字节    |  4字节   |   2字节    | 1字节  | 306字节 |   1字节   |



#### 4.2.2 头尾部设计

均采用大端序

发送者的IP，如`127.0.0.1`，那么就是`7F 00 00 01`

发送者的端口，采用2个字节表示`0-65532`之间的数据，如`11301`就是`2C 25`

接收者的同上

#### 4.2.3 帧长度分析

​	在设计的时候，我们对长度进行了讨论，按照`20/100000`，也就是`0.0002`的误码率来说，如果错一个帧，那么就是平均在5000个bit里面会出现一个，因此我们的帧就设置为5000一下为适合，由于每8个字节会在后面添加2个字节的校验位，因此我们的长度就设为400个字节，也就是3200bit，其中320字节是用于传输数据，80字节是用于校验
$$
13 Byte_{头部}+306Byte_{数据}+1Byte_{校验} = 320Byte_{未校验}\\
320\times \frac{10}{8} = 400Bytes\\
400Bytes = 400 \times 8  = 3200Bits
$$


#### 4.2.4 使用概率论进行误差分析

由于误码率是`20/100000`，即`0.0002`，如果出现了两个错误，且出现在一个`chunk`的一条线上，那么无法检测出来，运用概率论知识和`matlab`计算概率
$$
由于一帧具有3200bit，算是大数了，符合泊松分布\\
P(X= k) = \frac{e^{-\lambda} \lambda ^ k}{k!}\\
其中 \lambda = np = 3200*0.0002 = 0.64\\
当k = 2时,P(x=2) = 0.107989\\
在3200个比特之内，两个比特在一个chunk的概率为\\
\frac{1}{40} = 0.025\\
一个chunk内两个bit在一条线上的概率为\\
\frac{2 \times C_8^1\times C_9^2}{C_{80}^2} = 0.182278\\
那么遇见无法纠错的帧的概率为\\
0.107989\times0.025\times0.182278 = 0.00049210047355\\
几乎可以说是一个不可能事件了
$$

### 4.3 滑动窗口实现

#### 4.3.1 回退n协议

​	由于选择性重传的过于复杂，停等协议又过于简单粗暴，效率不高，我们采用了回退n的滑动窗口协议，协议内容如下

发送方发送一个滑动窗口大小的帧，如16个帧，分别添加帧序号

接收方接收到了一个帧，如果验证成功，发送一个`ACK.n`的信号，如果验证失败，发送一个`ERR.n`的信号

发送方在接收到`ACK.n`的时候运用滑动窗口协议，如

如果上一个是`ACK.4`，中间的`ACK.5`丢失了，这次接收到的是`ACK.6`，那么将滑动窗口拖动到`6+1=7`号窗口

如果上一个是`ACK.4`，这一个是`ERR.5`，说明第5帧有问题，滑动窗口拖动到5号窗口

滑动窗口拖动完成后，发送一个窗口中剩余的内容，重复以上行为，直到发送完成为止

#### 4.3.2 发送结束的确认

​	在发送方发送结束之后，接收方并不知道结束了，因此发送方需要发送一个结束符来表示发送结束，在这里我们经过讨论把结束符定义为`\xad\xff\xda`，并且加上前面的奇偶校验和帧信号之后进行发送，如果接受方接收到了这个信号，那么就可以认为是发送结束，于是断开连接，打印接收到的字符

代码如下

**发送方**

```python
def send(self,Text):
        size = 32
        frameNumber = 0
        lastendPtr = 0
        bytesText = method.text2Bytes(self,Text)
        binText = method.bytes2Bin(self,bytesText)
        Frames = self.bin2Frames(binText,306)#40 Unit,400-40*2-14=
        #initial send
        startPtr,currentPtr = 0,0
        endPtr = min(size,len(Frames))
        windows = [0]*size
        for i in range(endPtr):
            windows[i] = Frames[i]
            time.sleep(0.05)
            self.tcpLayer.sendControlCenter(self,self.dataWrap(windows[i],i))
        while(1):
            time.sleep(0.05)
            if(startPtr==endPtr):
                break
            respondRaw = self.bytes2Bin(self.tcp.sendSocket.recv(40000))
            respondbin = self.direction(respondRaw,bin(0xeeff)[2:],bin(0xffee)[2:])
            if(respondbin==-1):
                print('ack lost!')
                for i in range(lastendPtr,endPtr):
                    self.tcpLayer.sendControlCenter(self,self.dataWrap(Frames[i],i%size))
                    windows[i%size]=Frames[i]
                continue
            try:
                respondBytes,status,Info = self.tcpLayer.recvControlCenter(self,respondbin)
                respond = respondBytes.decode()
            except:
                print('respond parse ERR!',respondbin)
                for i in range(lastendPtr,endPtr):
                    self.tcpLayer.sendControlCenter(self,self.dataWrap(Frames[i],i%size))
                    windows[i%size]=Frames[i]
                continue
            print(respond)
            if(sum([ord(x) for x in list(respond.split('.')[0])])-sum([ord(x) for x in list('ACK')])<=8):
                #print(respond.split('.'))
                try:
                    carryNumber = int(respond.split('.')[1])-startPtr%size+1
                except:
                    print('respond number ERR!',respond)
                    for i in range(lastendPtr,endPtr):
                        self.tcpLayer.sendControlCenter(self,self.dataWrap(Frames[i],i%size))
                        windows[i%size]=Frames[i]
                    continue
                if(carryNumber)<0:
                    carryNumber+=size
                lastendPtr = endPtr
                endPtr = min(endPtr+carryNumber,len(Frames))
                startPtr +=carryNumber
                for i in range(lastendPtr,endPtr):
                    self.tcpLayer.sendControlCenter(self,self.dataWrap(Frames[i],i%size))
                    windows[i%size]=Frames[i]
            elif(respond.split('.')[0]=='ERR'):
                try:
                    self.tcpLayer.sendControlCenter(self,self.dataWrap(windows[int(respond.split('.')[1])+1],int(respond.split('.')[1])%size))
                except:
                    print('no ERR number!')
                    for i in range(lastendPtr,endPtr):
                        self.tcpLayer.sendControlCenter(self,self.dataWrap(Frames[i],i%size))
                        windows[i%size]=Frames[i]
                    continue
        finBytes = b'\xad\xff\xda'
        finAfterChunk = self.dataWrap(self.bin2Frames(self.bytes2Bin(finBytes),400)[0],frameNumber)
        self.tcpLayer.sendControlCenter(self,finAfterChunk)
        print('send is over...')
```

**接收方**

```python
def recv(self):
        recvText = b''
        size = 16
        frameNumber = 0
        while(1):
            time.sleep(0.05)
            rawBytes = self.sk.recv(40000)
            rawBins = self.bytes2Bin(rawBytes)
            afterDirect = self.direction(rawBins,bin(0xeeff)[2:],bin(0xffee)[2:])
            if(afterDirect==-1 or afterDirect == ''):
                statusInfo = (b'ERR.'+str(frameNumber).encode())
                waitForChunk = self.bin2Frames(self.bytes2Bin(statusInfo),400)
                afterChunk = self.dataWrap(waitForChunk[0],frameNumber)
                self.tcpLayer.sendControlCenter(self,afterChunk)
                continue
            onebytesText,status,frameInfo = self.tcpLayer.recvControlCenter(self,afterDirect)
            #print(frameInfo)
            if(onebytesText == b'\xad\xff\xda'):
                break
            frameNumber=int(status[0].split('.')[1])
            recvText+=onebytesText
            statusInfo = str(status[0]).encode()
            waitForChunk = self.bin2Frames(self.bytes2Bin(statusInfo),306)
            afterChunk = self.dataWrap(waitForChunk[0],frameNumber)
            self.tcpLayer.sendControlCenter(self,afterChunk)
        return recvText.decode()
```

#### 4.3.3 双工设计

​	在开始设计的时候我们在想如何让两个网元之间做到收发有来有回，受制于TCP流式传输的思想，我们想开两条信道来进行`客户端->服务端`和`服务端->客户端`的传输，但是由于一个套接字只能够绑定一个地址，这就是一个非常棘手的问题。而且一个程序在`socket.recv()`的时候是阻塞的，它无法干任何事情，更不要说一边听一边发了，这就是摆在我们眼前的一个问题，没法双工通信，就没法进行滑动窗口协议。

​	我们一开始的方案是额外建立一个套接字的TCP通道来发送`ACK.n`等信息，但是这个通道没有经过物理层模拟软件，没有任何差错，看上去是一种有点耍赖的方法，我们很快就放弃了这种方法。

​	我们想到的第二条路就是多线程，一个程序开两个线程，使用`python`的`threading`模块。但是这一想法在进行初步实施的时候，我们发现，我们初始化的`a = socket.socket(socket.AF_INET,socket.SOCK_STREAM)`在执行`a.accept()`的时候始终收不到连接信号，最后我们一步步排查，发现是这个模拟软件，只支持UDP的连接，不支持基于TCP的连接通信。

​	最后我们通过问老师，还有自己多次实验，了解到，当有数据包发过来的时候，并不是没有接收数据包就会丢下，而是会存在一个缓冲区里面，运行一次`a.recv()`就会接收一个数据包，于是我们通过先`recv()`后`send()`的方式，实现了基于UDP的双工通信

### 4.4 交换机设计

#### 4.4.1 转发表

​	由于转发表是交换机的工作核心，因此转发表我们需要一个能够进行一一映射的数据结构，在这里我们采用了python中的`dict`结构，也就是我们俗称的`哈希表`，能够通过`v[key] = value`的方式来对转发情况进行一一映射，由于元组结构无法作为哈希表的`key`，因此我们将这个结构转化为`string`字符串的形式，一个转发表大致如下

`table = {str(('127.0.0.1',13100)):('127.0.0.1',12101),str(('127.0.0.1',11100)):('127.0.0.1',12100)}`

通过`v[key] = value`的方式可以直接添加转发表，非常快捷。

#### 4.4.2 交换机工作原理

​	由于交换机需要一直接收并转发消息，因此传统的阻塞性的`socket.recv()`函数就不再适用，这里采用`select`函数来对`socket`进行底层的监听

Python中的select模块专注于I/O多路复用，提供了`select  poll  epoll`三个方法(其中后两个在Linux中可用，windows仅支持select)，另外也提供了`kqueue`方法(`freeBSD`系统)

进程指定内核监听哪些文件描述符(最多监听1024个`fd`)的哪些事件，当没有文件描述符事件发生时，进程被阻塞；当一个或者多个文件描述符事件发生时，进程被唤醒。

当我们调用`select()`时：

　　1 上下文切换转换为内核态

　　2 将`fd`从用户空间复制到内核空间

　　3  内核遍历所有`fd`，查看其对应事件是否发生

　　4  如果没发生，将进程阻塞，当设备驱动产生中断或者`timeout`时间后，将进程唤醒，再次进行遍历

　　5 返回遍历后的`fd`

　　6  将`fd`从内核空间复制到用户空间

通过`select()`，交换机可以随时检测到有消息的端口并接收数据包，交换机需要读取帧的目的地是否在自己的端口转发表内，如果在的话就根据转发表进行转发，如果不在的话就抛出错误，如果目的地是`('255.255.255.255':xxxxx)`的话，说明是广播信号，对所有的端口进行转播。

#### 4.3.3 层次化的编程设计

​	由于阶段二对数据进行了大量的处理，因此为了简化`main()`函数，我们将阶段二的代码进行了封装，封装成了`DCC`这样一个文件，然后我们就只需要调用`DCC.Unit()`即可初始化一个网元`DCC.start()`即可定义一个网元的功能，然后通过`a.send(text)`和`a.recv()`这样两个接口就可以实现发送和接收，对于上层的调用者来说，就相当于是输入一串字符，就能发送，运行`a.recv()`就能接受一个数据包，里面的校验，重传，滑动窗口对于上层的调用者来说是完全透明的，调用者只需要关注自己的设计就可以。

​	这样一来的结构化设计，使我们的交换机代码非常少

交换机代码如下

```python
import select
import DCC
dest1 = ('127.0.0.1',12100)
dest2 = ('127.0.0.1',12101)
b = DCC.Unit()
b.debug3()
table = {str(('127.0.0.1',13100)):('127.0.0.1',12101),str(('127.0.0.1',11100)):('127.0.0.1',12100)}
readable = [b.sk]
print('start....')
while(1):
    rlist,wlist,elist = select.select(readable,[],[],1)
    for sks in rlist:
        rawBytes = sks.recv(40000)
        rawBins = b.bytes2Bin(rawBytes)
        afterDirect = b.direction(rawBins,bin(0xeeff)[2:],bin(0xffee)[2:])
        if(afterDirect==-1):
            print('direct ERROR!')
            continue
        try:
            respondBytes,status,Info = b.tcpLayer.recvControlCenter(b,afterDirect)
            src = Info[1]
        except:
            continue
        if(str(src) in table):
            dst = table[str(src)]
            sendBytes = b'\xee\xff'+b.bin2Bytes(afterDirect)+b'\xff\xee'
            sks.sendto(sendBytes,dst)
            print(src,dst)
        elif(src[0]=='255.255.255.255'):
            for i in table:
                sendBytes = b'\xee\xff'+b.bin2Bytes(afterDirect)+b'\xff\xee'
                sks.sendto(sendBytes,table[i])
        else:
            print('no route')

```

### 4.4 路由器设计

#### 4.4.1 RIP协议

​	RIP(`Routing Information Protocol`,路由信息协议）是一种内部网关协议（IGP），是一种`动态路由选择协议`，用于自治系统（AS）内的路由信息的传递。RIP协议基于距离矢量算法（`DistanceVectorAlgorithms`），使用`跳数`来衡量到达目标地址的路由距离。这种协议的路由器只关心自己周围的世界，只与自己相邻的路由器交换信息，范围限制在15跳(15度)之内，再远，它就不关心了。

​	这里由于我们的跳数比较少，就没有设置范围限制。如何选择路由器之间发送路由表的时机，这是个问题，如果采用`time.sleep()`函数，那么这个程序就会被停止，这显然不是我们想要看到的。一种解决方案是获取系统时间，满足某一个条件进行一次发送，这样的话我们需要获取的权限较高，而且需要实时对获取到的时间进行处理，这样就造成了处理资源浪费，这不是我们想要看到的。另一种方案是使用`threading`来开辟一个线程来专门计时，这样就不会阻塞到程序的运行了。但是这样一来的程序会变得非常复杂，这个方案也被我们舍弃了。

​	最终我们采用的是随机数的方法，每个循环周期我们在0-10内取一个随机数，如果该数等于3，那么向周围发送自己的路由表。路由器在进行路由转发的时候如果发现这条信息的目的地是自己，那么就可以认为这是来自其他路由器的路由信息，于是读取帧信息，同自己的路由表进行合并。

#### 4.4.2 拓补结构

![image-20191221105600718](assets/image-20191221105600718.png)

​	我们设计了这样一个拓补结构，一个长条状，其中有ABCD四个子网，为了简便，每一个子网内配置一个机器，当然，要添加机器也是可以的。

​	从a1发送一张图片到d1，如果成功实现带有滑动窗口的传送图片，说明通信操作无误，路由器寻址正常，交换机正常，我们将这一目标作为我们的最终检验目标

#### 4.4.3 路由表结构

​	为了使函数调用的重复性降低，我们讲路由器相关的函数也封装成了一个文件`routetable.py`的形式，并给出了一系列的API来进行调用，这样一来我们的路由器函数就显得非常简洁。我们本来想要利用一个`struct`来存储一个路由表表项，但是`python`里面的`struct`的功能并非如此，于是我们用了`class`，来代替`struct`来实现我们想要的功能

```
routeTable
	|----destination (目的地)
	|----via (下一跳)
	|----cost(花费跳数)
```

##### 4.4.3.1 路由表函数——增删改查

​	由于路由表是一个`class`数组，因此路由表的增删改查就相当于是对数组的增删改查。

添加路由表的代码如下

```python
def addTable(dest, via, cost, table):
    r = routeTable()
    r.destination = dest
    r.via = via
    r.cost = cost
    table.append(r)
```

查询路由表的代码如下

```python
def findTables(item, tables):
    for i in tables:
        if(isInnerWeb(item,i.destination)):
            return i
    return False
```

##### 4.4.3.2 路由表函数——查询是否是内网

​	我们在进行路由表合并的时候非常需要判断那两项是一个内网的，如果是内网的话就需要我们进行合并，因此判断是否是内网这一函数起了关键作用，我们的判断方法是IP和端口号结合的方法，如果IP地址出现了不一样的话，就比较一方是否为0，若是0，那么就说明IP是子网。但是物理层模拟软件是通过端口号进行定位的，第一位是`1`，第二位代表设备号，第三位代表接口号，因此也讲端口号也考虑到内网的判断中，如果前两位相同，那么就说明这两个端口是在一个内网

查询是否是内网的代码如下

```python
def isInnerWeb(dest1,dest2):
    ip1 = dest1[0].split('.')
    ip2 = dest2[0].split('.')
    port1 = dest1[1]
    port2 = dest2[1]
    ipTrue = 1
    for i in range(4):
        int1 = int(ip1[i])
        int2 = int(ip2[i])
        if(int1!=int2):
            if(int1==0 or int2==0):
                continue
            else:
                ipTrue = 0
                break
    return (str(port1)[:2]==str(port2)[:2]) and (ipTrue)
```

##### 4.4.3.3 路由表函数——合并接收到的路由表

​	在进行路由表泛洪广播的时候我们需要将接收到的路由表同自己已有的路由表进行比对和合并，如果路由表是本地没有的，那么就在本地添加这个路由表，并且将下一跳的地址改写为发送该路由表的函数的地址，并且跳数+1，如果下一跳是自己或者是子网，那么就将这一条路由表省去。代码如下

```python
def mergeTables(localtables, recvtables, local, recvfrom): 
    add = 0
    for oneRecvTables in recvtables:
        add = 0
        for oneLocalTables in localtables:
            writeAble = not(isInnerWeb(oneLocalTables.destination, oneRecvTables.destination) or isInnerWeb(local,oneRecvTables.destination))
            if(writeAble):
                add+=1
        if(add == len(localtables)):
            addTable(oneRecvTables.destination,recvfrom,oneRecvTables.cost+1,localtables)

```

##### 4.4.3.4 路由表函数——路由表的打包与解包

​	我们需要将路由表进行打包发送出去，发送一个`class`显然是不现实的，因此我们将一个路由表项的三个参数，转化为字符串的形式，并定义一个分隔符`|`进行分割，接收方在接收到路由表之后只需要将其按照`|`进行分割，然后转化成为含有许多表项的`class`数组，然后同本地的路由表进行合并即可。代码实现如下

**打包**

```python
def packageTables(tables):
    txt = []
    for i in tables:
        txt.append(str(i.destination))
        txt.append(str(i.via))
        txt.append(str(i.cost))
    return '|'.join(txt)
```

**解包**

```python
def unpackageTables(rawString):
    tables = []
    dest,via,cost = '','',''
    split = rawString.split('|')
    for i in range(len(split)):
        cnt = i%3
        if(cnt==0):
            dest = eval(split[i])
        elif(cnt==1):
            via = eval(split[i])
        elif(cnt==2):
            cost = int(split[i])
            addTable(dest,via,cost,tables)
    return tables
```

##### 4.4.3.5 路由表函数——路由表的冒泡排序与去重

​	我们在进行路由表的展示的时候，发现路由表是根据加入的顺序排列的，非常杂乱无章，我们希望按照路由表的`IP>PORT>COST`来进行一个排序，因此我们需要编写一个冒泡排序的函数来对路由表进行一个排序，但是`python`并不支持`C++`的`重载运算符`的功能，因此我们自己编写了一个类似于`>`的函数`aboveTable(tuble1,tuble2)->bool`用来判断两个路由表项的先后关系，最后使用冒泡排序来进行排序

​	去重也是我们需要考虑的，虽然按照上述的几乎不会有重复项，但是我们在实验的时候还是发现了重复项，因此我们在路由表展示的时候添加了一个去重代码，来保证一个路由表项没有重复的。代码如下

```python
def aboveTable(tuble1, tuble2):
    ips1 = tuble1.destination[0].split('.')
    ips2 = tuble2.destination[0].split('.')
    for i in range(len(ips1)):
        if(int(ips1[i])>int(ips2[i])):
            return True
    port1 = tuble1.destination[1]
    port2 = tuble2.destination[1]
    if(port1>port2):
        return True
    else:
        return False

def sortTable(tables):
    lens = len(tables)
    for i in range(lens):
        for j in range(0,lens-i-1):
            if(aboveTable(tables[j],tables[j+1])):
                tables[j],tables[j+1] = tables[j+1],tables[j]
                
def showTable(tables):
    sortTable(tables)
    for onetable in tables:
        if(tables.count(onetable)>=2):
            tables.pop(tables.index(onetable))
    for i in tables:
        print(str(i.destination),str(i.via),str(i.cost))
```

#### 4.4.4 具体泛洪分析

现在假设我们有上图的A,B,C,D四个路由节点，路由节点的配置为

**A（192.1.1.1）：**

| dest      | via       | cost |
| --------- | --------- | ---- |
| 192.1.2.0 | 192.1.2.1 | 1    |

**B(192.1.2.1):**

| dest      | via       | cost |
| --------- | --------- | ---- |
| 192.1.1.0 | 192.1.1.1 | 1    |
| 192.1.3.0 | 192.1.3.1 | 1    |

**C（192.1.3.1）：**

| dest      | via       | cost |
| --------- | --------- | ---- |
| 192.1.2.0 | 192.1.2.1 | 1    |
| 192.1.4.0 | 192.1.4.1 | 1    |

**D(192.1.4.1):**

| dest      | via       | cost |
| --------- | --------- | ---- |
| 192.1.3.0 | 192.1.3.1 | 1    |

---

第一次泛洪

A->B发送路由表，B路由表不变

B->A发送路由表，A的路由表更新为

| dest      | via       | cost |
| --------- | --------- | ---- |
| 192.1.2.0 | 192.1.2.1 | 1    |
| 192.1.3.0 | 192.1.2.1 | 2    |

B->C发送路由表，C的路由表更新为

| dest      | via       | cost |
| --------- | --------- | ---- |
| 192.1.2.0 | 192.1.2.1 | 1    |
| 192.1.4.0 | 192.1.4.1 | 1    |
| 192.1.1.0 | 192.1.2.1 | 2    |

C->B发送路由表，B的路由表更新为

| dest      | via       | cost |
| --------- | --------- | ---- |
| 192.1.1.0 | 192.1.1.1 | 1    |
| 192.1.3.0 | 192.1.3.1 | 1    |
| 192.1.4.0 | 193.1.3.1 | 2    |

C->D发送路由表，D的路由表更新为

| dest      | via       | cost |
| --------- | --------- | ---- |
| 192.1.1.0 | 192.1.3.1 | 3    |
| 192.1.2.0 | 192.1.3.1 | 2    |
| 192.1.3.0 | 192.1.3.1 | 1    |

D->C发送路由表，C路由表不变

---

第二次泛洪

A->B发送路由表，B路由表不变

B->A发送路由表，A路由表变为

| dest      | via       | cost |
| --------- | --------- | ---- |
| 192.1.2.0 | 192.1.2.1 | 1    |
| 192.1.3.0 | 192.1.2.1 | 2    |
| 192.1.4.0 | 192.1.2.1 | 3    |

B->C发送路由表，C路由表不变

C->B发送路由表，B路由表不变

C->D发送路由表，D路由表不变

D->C发送路由表，C路由表不变

---

经过两次泛洪，A,B,C,D的路由表更新为

A

| dest      | via       | cost |
| --------- | --------- | ---- |
| 192.1.2.0 | 192.1.2.1 | 1    |
| 192.1.3.0 | 192.1.2.1 | 2    |
| 192.1.4.0 | 192.1.2.1 | 3    |

B

| dest      | via       | cost |
| --------- | --------- | ---- |
| 192.1.1.0 | 192.1.1.1 | 1    |
| 192.1.3.0 | 192.1.3.1 | 1    |
| 192.1.4.0 | 192.1.4.1 | 2    |

C

| dest      | via       | cost |
| --------- | --------- | ---- |
| 192.1.1.0 | 192.1.2.1 | 2    |
| 192.1.2.0 | 192.1.2.1 | 1    |
| 192.1.4.0 | 192.1.4.1 | 1    |

D

| dest      | via       | cost |
| --------- | --------- | ---- |
| 192.1.1.0 | 192.1.3.1 | 3    |
| 192.1.2.0 | 192.1.3.1 | 2    |
| 192.1.3.0 | 192.1.3.1 | 1    |

这样经过泛洪就完成了整个网络中子网与路由的获取，由于实际情况我们的物理层模拟软件在本地上面跑，只能够通过port来定位的方式来完成子网与寻址。

#### 4.4.5 物理层模拟软件的一键启动

​	由于我们定义了8个网元，因此我们需要启动`4 + 2 + 3 + 3 + 2 = 14`个物理层模拟软件，如果我们使用手动配置的话非常麻烦，需要我们每一次在启动的时候配置14个网元的信息，因此我们阅读了指导书上的`4.2 利用配置文件简化程序的初始化操作——ne.txt`的说明，来自定义了一个物理层模拟软件的配置文件，其中端口号分配如图所示

![image-20191221202608607](assets/image-20191221202608607.png)

由于文件太长，我们在`ne.txt`中编写的文件放于`附1`中

最后我们通过程序包里面的`oneKey2Go.exe`就可以一键启动我们的网元

也可以采用`python`中的`pywin32.win32api`来运行

`win32api.shellexecute('0','open','PHY.exe','1 0 1','','1')`

​	其中最后三个参数是物理层的设备号，端口号，是否打开新窗口。我们也采用了这样的方式来启动了我们的四个路由器的`python`程序，但是在调试的时候，由于`shellexecute()`中执行的`cmd`窗口一旦遇上异常或错误就会在很快的时间内抛出错误并退出，不利于我们查看调试信息。于是我们在调试的时候，选择在`powershell`中执行`python Arouter.py`这样的方式来执行，这样执行的好处是程序发生错误之后报错信息会留在`powershell`上面，我们就能够方便地查看错误信息，缺点就是我们需要开多个窗口手动输入运行的命令。

### 4.5 发送图片的设计

#### 4.5.1 图片打开的格式

​	现在的图片普遍都是JPG，或者是PNG，如何将图片转化成比特流的方式来发送是我们需要考虑的问题。我们使用`winhex`打开一张图片就可以发现

![image-20191221205624641](assets/image-20191221205624641.png)

​	除了图片的元信息之外，图片中包含了大量的不可见字符，而这些不可见字符中很有可能有我们的`定位符`，`结束符`等等的特殊控制字符，直接发送二进制比特数据，这一方案显然不可行。

我们想到了一个常用的编码，`base64`编码

#### 4.5.2 base64介绍

​	目前`Base64`已经成为网络上常见的传输`8Bit`字节代码的编码方式之一。在做支付系统时，系统之间的报文交互都需要使用`Base64`对明文进行转码，然后再进行签名或加密，之后再进行（或再次`Base64`）传输。那么，`Base64`到底起到什么作用呢？

​	在参数传输的过程中经常遇到的一种情况：使用全英文的没问题，但一旦涉及到中文就会出现乱码情况。与此类似，网络上传输的字符并不全是可打印的字符，比如二进制文件、图片等。`Base64`的出现就是为了解决此问题，它是基于`64`个可打印的字符来表示二进制的数据的一种方法。

​	电子邮件刚问世的时候，只能传输英文，但后来随着用户的增加，中文、日文等文字的用户也有需求，但这些字符并不能被服务器或网关有效处理，因此`Base64`就登场了。随之，`Base64`在URL、Cookie、网页传输少量二进制文件中也有相应的使用。

#### 4.5.3 使用base64对图片进行编码和解码

我们使用python自带的base64库来进行图片数据流的编码与解码，代码如下

```python
import base64

def picEncodeBase64(path):
    file = open(path,'wb')
    base = base64.b64encode(file.read())
    file.close()
    return base

def decodePic(bins,picType):
    imgdata = base64.b64decode(bins)
    file = open('.\\out.'+picType,'wb')
    file.write(imgdata)
    file.close()
    print('pic is saved in .\\out.xxx')

```

我们将这两个常用的功能封装成函数形式方便调用，我们试着打开一个`PNG`图片

![image-20191221210353443](assets/image-20191221210353443.png)

然后通过`base64`编码之后得到的结果如下

![image-20191221210711392](assets/image-20191221210711392.png)

说明编码成功，随后我们将输出使用`base64.b64decode()`解码并写入`out.png`，打开文件，发现就是之前编码的图片文件

![image-20191221211032841](assets/image-20191221211032841.png)

## 五.实验结果

### 5.1 实验测试方案

​	我们的实验时间是环环相扣的，我们在进行成帧设计的时候会用到阶段一要求的套接字编程，进行交换机的时候会用到阶段二的滑动窗口，编写路由器的时候会用到二层交换机，因此我们只需要从我们构建的网元的`a1`发送一张图片到`d1`，并`观测沿路的路由信息`，`查看图片传输结果`即可判断是否传输成功

### 5.2 实验测试步骤

#### 5.2.1 一键启动物理层模拟软件

将我们的`ne.txt`导入进`Onekey2Go.exe`文件夹运行

![image-20191221212119547](assets/image-20191221212119547.png)

摆放非常混乱，我们按照我们信道的要求在另一块屏幕上面摆出我们想要的样子

![image-20191221212345793](assets/image-20191221212345793.png)

这样就可以在一块屏幕上观看路由表，另一块屏幕上查看发送情况了

#### 5.2.2 一键启动四个路由器并观察泛洪

![image-20191221212601712](assets/image-20191221212601712.png)

可以看见，四个路由器都有效识别出了整个线路的路由信息并不断打印出来，说明实现了`基于RIP的路由`，我们只能通过调整窗口大小的方式来获得最佳观看效果，如果有`tmux`这样的分屏利器观察这样多个`shell`的信息就好得多

#### 5.2.3 发送数据，观察路由信息

我们试着传输一串中英日语夹杂的字符进去，从A传输到D

![image-20191221213049340](assets/image-20191221213049340.png)

我们可以看到数据包在两个主机之间往来的路由数据，说明实现了`基于RIP的动态路由的寻址`

A1

```python
import DCC
A = DCC.Unit()
local = ('127.0.0.1', 11200)
datalink = ('127.0.0.1', 11201)
dest = ('127.0.0.1', 14200)
A.debug4(local, dest, datalink)
print('A.start to send')
A.send('aaa这是中文こんばんは...\n'*10)
aa = input('end...')
```

D1

```python
import DCC
D = DCC.Unit()
local = ('127.0.0.1', 14200)
datalink = ('127.0.0.1', 14201)
dest = ('127.0.0.1', 11200)
D.debug4(local, dest, datalink)
print('D.start to recv')
print(D.recv())
res = input('end...')
```



![image-20191221213208931](assets/image-20191221213208931.png)

可以看到，不仅实现了`点对点的路由`和`交换机`，而且`滑动窗口协议`也实现了。

#### 5.2.4 传输图片验证

​	要发送的图片是一个PNG，如下

![p0](assets/p0-1576937894492.png)

​	由于我们的图片比较大，加上校验我们需要非常长的一段时间来去检验和封包，然后接收到了一堆数据包之后我们也需要非常长的时间去检验和解包，还好我们搞到了一个具有双路`E5 2660 v4`的28核服务器，跑了半个小时，最后我们得到的结果如下

![image-20191221221640629](assets/image-20191221221640629.png)

然后我们找到目录下的`out.png`

![image-20191221223058053](assets/image-20191221223058053.png)

发现图片信息完整，滑动窗口协议完整，但是执行的时间非常长

![image-20191221223421235](assets/image-20191221223421235.png)

在这样一个CPU上面跑满了半个小时才跑完，是因为我们的算法过于复杂，不适合一次性传输特大的帧，只适合一次慢慢传输1K以内大小的帧。

## 六、总结与反思

### 6.1 设计过程

​	我们在设计的时候这些描述，看上去轻描淡写，一笔带过，其实经过了很多次调BUG，找问题，调BUG的过程，上面的代码几乎重写过3遍。前期我们仅仅实现了帧定位和二位奇偶校验，而且代码写的很混乱。后面要添加功能的时候发现根本没法在原来的基础上进行重构，因此我们只能对之前的代码进行重构，重新理清思路。

​	在使用类中类的时候，我们也遇到了一大堆棘手的问题，`self`指代的对象不明，一个函数中10行代码能出现20个`self`，这些`self`一旦搞不清就很容易代码出错，而且python的类中类的调用异常复杂，又是继承又是父类又是派生类的，这就是追求实现API简洁的后果，在后期设计交换机的时候我们抛弃了全部代码一个文件的做法，改成了多文件然后给出API的方式，这样一来我们的程序的易用性和间接性得到了极大的提高。上面的血泪教训耗费了我们大量的时间，好几个不眠之夜在修改代码，调试，推翻重来上，同时也证明了提前规划的重要性

​	在设计路由算法的时候，我们试着提前规划我们的功能，对每一个地方先用笔记本模拟通了，之后再一一写程序去本地调试，最后上物理层模拟软件的方式，最后路由算法是我们写的最为顺畅的一部分。

### 6.2 大数据传输

​	正如上面的例子，一个`687kb`的文件，我们在一个强劲的CPU上花了半个小时去计算和纠错，是因为我们的算法里面大量采用了重复遍历的方式，没有考虑到时间复杂度，因此导致了计算量巨大。但是联想到实际生活中，我们的图片也好，视频也好其实是分片加载的，如果我们可以将图片分割成1K大小的数据进行分片传输可能会更好。而且在算法方面我们的代码还可以运用`数据结构与算法`中的知识进行时间复杂度的优化。

### 6.3 流量控制与寻址

​	由于我们采用了滑动窗口协议，但是我们的滑动窗口协议的窗口大小是固定的，因此我们并没有完全模拟到现实的滑动窗口大小增减情况

## 附1 ne.txt

