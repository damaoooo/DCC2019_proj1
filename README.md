# 项目二文件结构

```
|-- Python 项目二
	|-- Unit 网元
		|-- tcpLayer网络层
			checkXor(str:text)->bool:res
		|-- dataLayer 数据链路层
			|-- wrapFrame(rawFrames)->list:Frames
			|-- parseFrame(recvFrames)->list:checkedFrames
	|-- method 方法
		|--Oddcheck(list:Frames)->list:result[[row],[crowd]]
		|--bytes2Bin(bytestr:bytes)->str:rawBin
		|--bin2Frames(str:bindata,mode)->list:Frames//mode->1.encode 2.decode
		|--frames2Bin(list:Frames)->str:rawBin
		|--bin2Bytes(str:rawBin)->bytes:bytes
		|--text2Bytes(str:bytes)->str:bytes
		|--addXorCheck(str:text)->str:text
```

按帧传输一帧8\*8 bit + 2\*8校验位 = 80bit，二维奇偶校验

或者是采用16\*16+2*16 = 288bit，由于UTF-8编码问题有ASCII字符是8bit，所以就可能会出现只有8bit而不是16bit，就采用在最后面加入8个0的方式进行区分

数据链路层：

text->text2Bytes()->bytes2Bin()->bin2Frames()->Frame->oddcheck->bin->bytes->send

recv->bin->Frame->oddcheck()->checkXor()->Frame2bin()->bin2bytes()->bytes2text()

网络层：

sender: send->recv->send

recver : recv->send : ack->recv()