import sys
import argparse
from yolo import YOLO, detect_video
from PIL import Image

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from tutorial import Calculator
from tutorial.ttypes import InvalidOperation
import threading

import base64
import io
import os


def parse():
    # 传入参数的方法，不用管，都是用默认的参数
    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''
    parser.add_argument(
        '--model', type=str,
        help='path to model weight file, default ' +
        YOLO.get_defaults("model_path")
    )

    parser.add_argument(
        '--anchors', type=str,
        help='path to anchor definitions, default ' +
        YOLO.get_defaults("anchors_path")
    )

    parser.add_argument(
        '--classes', type=str,
        help='path to class definitions, default ' +
        YOLO.get_defaults("classes_path")
    )

    parser.add_argument(
        '--gpu_num', type=int,
        help='Number of GPU to use, default ' +
        str(YOLO.get_defaults("gpu_num"))
    )
    return parser


# 定义4和全局变量用于程序线程之间相互传递
# forward 代码由server线程向主线程进行传递
# back  代码由主线程向 server线程进行传递
# container 是一个容器类型，用于数据的传输
# exchanger 是一个交换的容器，用于数据交换
forward = []
back = {}
container = []
exchanger = {}

# 这个是thrift的一个类

class CalculatorHandler:

    # 初始化类

    def __init__(self):
        self.log = {}

    # 定义一个方法，接受到客户端发过来的参数
    # ip 是传过来的视频的ip字段
    # time 是当前截屏的时间字段
    # uuid 是唯一标识符，用于后面对不使用
    # win1 是用于判断是不是预留窗口的数据，如果win1 = 0 ，则这个窗口是预留窗口，返回对应的数据，如果 win1 = 1，这个这个窗口是正常窗口
    # win2 是用于判断是不是这个窗口有三个人，如果 win2=0 表示只有两个窗口。如果 win2 = 1， 表示有三个窗口
    # 根据 win1 和 win2 的情况做判断

    def registe(self, ip, time, uuid, imgBinary, winLeft, winMiddle, winRight):
        global forward
        global back
        global container
        global exchanger
        container = []

        result = {}
        result['ip'] = ip
        result["time"] = time
        result['uuid'] = uuid

        forward.append(1)
        container.append(imgBinary)

        # 添加一个可以保存文件的路径
        path = f"/home/video/save_img/{time[:8]}/"
        folder = os.path.exists(path)
        # 判断是否存在文件夹如果不存在则创建为文件夹
        if not folder:
            # makedirs 创建文件时如果路径不存在会创建这个路径
            os.makedirs(path)
        # 保存图片的路径及文件名
        saveImgUrl = os.path.join(path, f"{ip + '-' + time}.jpg")
        result['saveImgUrl'] = "None"

        def save_img(imgBinary,saveImgUrl):
            # 如果识别到只有一个人，保存图片到服务器上
            image = io.BytesIO(imgBinary)
            img = Image.open(image)
            img.save(saveImgUrl, quality=95)
            

        while True:
            if back != {}:
                forward = []
                print(back)
                exchanger = back
                back = {}
                # 如果返回值有错误则返回 error
                if 'error' in exchanger:
                    return {"error": "error"}

                # 判断这个窗口是不是预留窗口 如果是预留窗口，则返回 -1 ， 表示预留窗口                
                # 先判断第一个窗口的数据，1 表示正常， -1 表示预留窗口 ，0 表示没有这个窗口
                if winLeft == 1:
                    # 如果只有一个窗口
                    if winMiddle == 0 and winRight == 0:
                        if int(exchanger['person']) >= 1:
                            result["winLeft"] = '1'
                            result["winMiddle"] = '-'
                            result["winRight"] = '-'
                            return result

                        elif int(exchanger['person']) == 0:
                            save_img(imgBinary,saveImgUrl)
                            result['saveImgUrl'] = saveImgUrl
                            result["winLeft"] = '0'
                            result["winMiddle"] = '-'
                            result["winRight"] = '-'
                            return result

                        else:
                            save_img(imgBinary,saveImgUrl)  
                            result['saveImgUrl'] = saveImgUrl                          
                            return {"person number": " is error"}
                    
                    # 如果其他两个都是预留窗口
                    elif winMiddle == -1 and winRight == -1:
                        if int(exchanger['person']) >= 1:
                            result["winLeft"] = '1'
                            result["winMiddle"] = '-1'
                            result["winRight"] = '-1'
                            return result

                        elif int(exchanger['person']) == 0:
                            save_img(imgBinary,saveImgUrl)
                            result['saveImgUrl'] = saveImgUrl
                            result["winLeft"] = '0'
                            result["winMiddle"] = '-1'
                            result["winRight"] = '-1'
                            return result


                        else:
                            save_img(imgBinary,saveImgUrl)
                            result['saveImgUrl'] = saveImgUrl
                            return {"person number": " is error"}

                    # 如果三个窗口都是正常的
                    elif winMiddle == 1 and winRight == 1: 
                        if int(exchanger['person']) >= 3:
                            result["winLeft"] = '1'
                            result["winMiddle"] = '1'
                            result["winRight"] = '1'
                            return result


                        elif int(exchanger['person']) == 2:
                            save_img(imgBinary,saveImgUrl)
                            result['saveImgUrl'] = saveImgUrl
                            if 0 < float(exchanger["person1"]) < 0.33 and 0.33 <= float(exchanger["person2"]) < 0.66:
                                result["winLeft"] = '1'
                                result["winMiddle"] = '1'
                                result["winRight"] = '0'
                                return result

                            elif 0.33 <= float(exchanger["person1"]) < 0.66 and 0.66 <= float(exchanger["person2"]) < 1:
                                result["winLeft"] = '0'
                                result["winMiddle"] = '1'
                                result["winRight"] = '1'
                                return result


                            elif 0.66 <= float(exchanger["person1"]) < 1 and 0 < float(exchanger["person2"]) < 0.33:
                                result["winLeft"] = '1'
                                result["winMiddle"] = '0'
                                result["winRight"] = '1'
                                return result


                        elif int(exchanger['person']) == 1: 
                            save_img(imgBinary,saveImgUrl)
                            result['saveImgUrl'] = saveImgUrl
                            if 0 < float(exchanger["person1"]) < 0.33:
                                result["winLeft"] = '1'
                                result["winMiddle"] = '0'
                                result["winRight"] = '0'
                                return result

                            elif 0.33 <= float(exchanger["person1"]) < 0.66:
                                result["winLeft"] = '0'
                                result["winMiddle"] = '1'
                                result["winRight"] = '0'
                                return result

                            elif 0.66 <= float(exchanger["person1"]) < 1:
                                result["winLeft"] = '0'
                                result["winMiddle"] = '0'
                                result["winRight"] = '1'
                                return result

                        else:
                            save_img(imgBinary,saveImgUrl)
                            result['saveImgUrl'] = saveImgUrl
                            return {"person number": " is error"}

                    # 如果中间的窗口没有人，右边的窗口是正常的 
                    elif (winMiddle == 0 and winRight == 1):
                        if int(exchanger['person']) >= 2:
                            result["winLeft"] = '1'
                            result["winMiddle"] = '-'
                            result["winRight"] = '1'
                            return result


                        elif int(exchanger['person']) == 1:
                            save_img(imgBinary,saveImgUrl)
                            result['saveImgUrl'] = saveImgUrl
                            if 0 < float(exchanger["person1"]) < 0.5:
                                result["winLeft"] = '1'
                                result["winMiddle"] = '-'
                                result["winRight"] = '0'
                                return result

                            else:
                                result["winLeft"] = '0'
                                result["winMiddle"] = '-'
                                result["winRight"] = '1'
                                return result

                        
                        elif int(exchanger['person']) == 0:
                            save_img(imgBinary,saveImgUrl)
                            result['saveImgUrl'] = saveImgUrl
                            result["winLeft"] = '0'
                            result["winMiddle"] = '-'
                            result["winRight"] = '0'
                            return result


                        else:
                            save_img(imgBinary,saveImgUrl)
                            result['saveImgUrl'] = saveImgUrl
                            return {"person number": " is error"}
                    
                    # 如果中间的窗口没有人，右边的窗口是预留的 
                    elif (winMiddle == 0 and winRight == -1):
                        if int(exchanger['person']) >= 1:
                            result["winLeft"] = '1'
                            result["winMiddle"] = '-'
                            result["winRight"] = '-1'
                            return result


                        elif int(exchanger['person']) == 0:
                                                    
                            result["winLeft"] = '0'
                            result["winMiddle"] = '-'
                            result["winRight"] = '-1'
                            save_img(imgBinary,saveImgUrl)  
                            result['saveImgUrl'] = saveImgUrl  
                            return result

                    
                    # 如果中间的窗口正常的，右边的窗口是预留的 
                    elif(winMiddle == 1 and winRight == -1):
                        if int(exchanger['person']) >= 2:
                            result["winLeft"] = '1'
                            result["winMiddle"] = '1'
                            result["winRight"] = '-1'
                            return result


                        elif int(exchanger['person']) == 1:
                            save_img(imgBinary,saveImgUrl)
                            result['saveImgUrl'] = saveImgUrl
                            if 0 < float(exchanger["person1"]) < 0.5:
                                result["winLeft"] = '1'
                                result["winMiddle"] = '0'
                                result["winRight"] = '-1'
                                return result

                            else:
                                result["winLeft"] = '0'
                                result["winMiddle"] = '1'
                                result["winRight"] = '-1'
                                return result

                        
                        elif int(exchanger['person']) == 0:
                            save_img(imgBinary,saveImgUrl)
                            result['saveImgUrl'] = saveImgUrl
                            result["winLeft"] = '0'
                            result["winMiddle"] = '0'
                            result["winRight"] = '-1'
                            return result

                        else:
                            save_img(imgBinary,saveImgUrl)
                            result['saveImgUrl'] = saveImgUrl
                            return {"person number": " is error"}
                    
                    # 如果中间的窗口预留的，右边的窗口是正常的
                    elif (winMiddle == -1 and winRight == 1): 
                        if int(exchanger['person']) >= 2:
                            result["winLeft"] = '1'
                            result["winMiddle"] = '-1'
                            result["winRight"] = '1'
                            return result


                        elif int(exchanger['person']) == 1:
                            save_img(imgBinary,saveImgUrl)
                            result['saveImgUrl'] = saveImgUrl
                            if 0 < float(exchanger["person1"]) < 0.5:
                                result["winLeft"] = '1'
                                result["winMiddle"] = '-1'
                                result["winRight"] = '0'
                                return result

                            else:
                                result["winLeft"] = '0'
                                result["winMiddle"] = '-1'
                                result["winRight"] = '1'
                                return result

                        
                        elif int(exchanger['person']) == 0:
                            save_img(imgBinary,saveImgUrl)
                            result['saveImgUrl'] = saveImgUrl
                            result["winLeft"] = '0'
                            result["winMiddle"] = '-1'
                            result["winRight"] = '0'
                            return result
                        

                        else:
                            save_img(imgBinary,saveImgUrl)
                            result['saveImgUrl'] = saveImgUrl
                            return {"person number": " is error"}

                # 第一个窗口是预留窗口  
                elif winLeft == -1:
                    # 如果一个窗口
                    if winMiddle == 0 and winRight == 0:                        
                        result["winLeft"] = '-1'
                        result["winMiddle"] = '-'
                        result["winRight"] = '-'
                        save_img(imgBinary,saveImgUrl)  
                        result['saveImgUrl'] = saveImgUrl  
                        return result

                        
                    # 如果其他两个都是预留窗口
                    elif winMiddle == -1 and winRight == -1:
                        result["winLeft"] = '-1'
                        result["winMiddle"] = '-1'
                        result["winRight"] = '-1'
                        save_img(imgBinary,saveImgUrl)
                        result['saveImgUrl'] = saveImgUrl
                        return result


                    # 如果其他两个窗口都是正常的
                    elif winMiddle == 1 and winRight == 1: 
                        if int(exchanger['person']) >= 2: 
                            result["winLeft"] = '-1'
                            result["winMiddle"] = '1'
                            result["winRight"] = '1'
                            return result


                        elif int(exchanger['person']) == 1: 
                            save_img(imgBinary,saveImgUrl)
                            result['saveImgUrl'] = saveImgUrl
                            if 0.33 <= float(exchanger["person1"]) < 0.66:
                                result["winLeft"] = '-1'
                                result["winMiddle"] = '1'
                                result["winRight"] = '0'
                                return result


                            elif 0.66 <= float(exchanger["person1"]) < 1:
                                result["winLeft"] = '-1'
                                result["winMiddle"] = '0'
                                result["winRight"] = '1'
                                return result

                        else:
                            save_img(imgBinary,saveImgUrl)
                            result['saveImgUrl'] = saveImgUrl
                            return {"person number": " is error"}

                    # 如果中间的窗口没有人，右边的窗口是正常的 
                    elif (winMiddle == 0 and winRight == 1):
                        if int(exchanger['person']) >= 1:
                            result["winLeft"] = '-1'
                            result["winMiddle"] = '-'
                            result["winRight"] = '1'
                            return result

                        
                        elif int(exchanger['person']) == 0:
                            save_img(imgBinary,saveImgUrl)
                            result['saveImgUrl'] = saveImgUrl
                            result["winLeft"] = '-1'
                            result["winMiddle"] = '-'
                            result["winRight"] = '0'
                            return result


                        else:
                            save_img(imgBinary,saveImgUrl)
                            result['saveImgUrl'] = saveImgUrl
                            return {"person number": " is error"}
                    
                    # 如果中间的窗口没有人，右边的窗口是预留的 
                    elif (winMiddle == 0 and winRight == -1):
                        
                        result["winLeft"] = '-1'
                        result["winMiddle"] = '-'
                        result["winRight"] = '-1'
                        return result


                    # 如果中间的窗口正常的，右边的窗口是预留的 
                    elif(winMiddle == 1 and winRight == -1):
                        if int(exchanger['person']) >= 1:
                            result["winLeft"] = '-1'
                            result["winMiddle"] = '1'
                            result["winRight"] = '-1'
                            return result


                        elif int(exchanger['person']) == 0:
                            save_img(imgBinary,saveImgUrl)
                            result['saveImgUrl'] = saveImgUrl
                            result["winLeft"] = '-1'
                            result["winMiddle"] = '0'
                            result["winRight"] = '-1'
                            return result


                        else:
                            save_img(imgBinary,saveImgUrl)
                            result['saveImgUrl'] = saveImgUrl
                            return {"person number": " is error"}
                    
                    # 如果中间的窗口预留的，右边的窗口是正常的
                    elif (winMiddle == -1 and winRight == 1): 
                        if int(exchanger['person']) >= 1:
                            result["winLeft"] = '-1'
                            result["winMiddle"] = '-1'
                            result["winRight"] = '1'
                            return result

                            
                        elif int(exchanger['person']) == 0:
                            save_img(imgBinary,saveImgUrl)
                            result['saveImgUrl'] = saveImgUrl
                            result["winLeft"] = '-1'
                            result["winMiddle"] = '-1'
                            result["winRight"] = '0'
                            return result


                        else:
                            save_img(imgBinary,saveImgUrl)
                            result['saveImgUrl'] = saveImgUrl
                            return {"person number": " is error"}
                else:
                    return {"parameter": " is error"}
                print(result)       
                break
            else:
                pass


def detect_img():

    # 这个一个主循环的方法，
    # 单独开启这个线程
    # 有一个主循环程序，用于一直执行，并且把模型一直加载cpu上面

    FLAGS = parse()
    yolo = YOLO(**vars(FLAGS))
    global forward
    global back
    global container
    global exchanger
    while True:
        if len(forward) == 1:
            try:
                img = io.BytesIO(container[0])
                image = Image.open(img)
                forward = []
                # print(c[0][:10])
                back = yolo.detect_image(image)
                # print("@@@@@@@")
                container = []
            except Exception as e:
                print(e, '********')
                forward = []
                container = []
                back['error'] = "error"
                pass
        else:
            pass
    yolo.close_session()


if __name__ == '__main__':
    # thrift的代码
    handler = CalculatorHandler()
    processor = Calculator.Processor(handler)
    transport = TSocket.TServerSocket(host='10.127.93.10', port=8090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)
    # 开启服务
    print('Starting the server...')
    # 创建一个线程
    thread1 = threading.Thread(target=detect_img, name="线程1")

    # 创建线程完毕之后，一定要启动
    thread1.start()
   
    # thread2 = threading.Thread(target = server.serve)
    # thread2.start()
    server.serve()
    print('done.')
