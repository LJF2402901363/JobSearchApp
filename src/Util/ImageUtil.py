from PIL import Image


class ImageUtil:
    @staticmethod
    def imageScale(srcImagePath,desImagePath,widthScale,heightScale):
        """
        将源路径srcImagePath图片按照原来图片的宽和高按照指定的比例widthScale,heightScale缩小或者放大，然后写入到指定的desImagePath文件路径中去
        :param srcImagePath: 源图片的路径
        :param desImagePath: 缩放后存放图片的路径
        :param widthScale: 图片的宽放大或缩小的比例
        :param heightScale: 图片的高放大或缩小的比例
        :return:
        """
        # 加载图片
        img = Image.open(srcImagePath,mode="r")
        # 获取图片的宽
        width = img.size[0]
        # 获取图片的高
        height = img.size[1]
        # 进行缩放或者放大
        out = img.resize((width*widthScale,height*heightScale))
        # 保存缩放后的图片到指定的路径
        out.save(desImagePath)

