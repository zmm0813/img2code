1. yolo.py是YOLOX网络，也是本研究的元素识别网络，nets和utils两个文件夹是YOLOX会用到的一些文件。

2. model_data中的best_epoch_weights.pth是YOLOX会用到的权重文件，model_data中的voc_classes.txt记录了元素识别部分需要识别的元素类别。

3. img中会保存元素识别所识别得到的元素的截图，用于对每个元素进行样式推理。

4. code_generation是生成代码的文件夹：

   - image中的real.jpg是输入图片。
   - annotations用来存放元素识别的结果xml文件。

   - detect_str.py是识别元素文本内容的文件，调用了百度的OCR库。

   - get_color.py是获取背景颜色的文件。

   - model.py是样式推理网络，ResNet34。

   - radius.pth是推理边框圆角的网络的权重文件。

   - font.pth是推理字体大小的网络的权重文件。
   - predict_font.py是预测字体大小的文件。
   - predict_radius.py是预测边框圆角的文件。

   - myhtml是生成的html代码。

   - mystyle.css是生成的css代码。
   - 代码生成.py是生成代码的文件。在生成代码时，运行生成代码的文件，
     - 可以手动修改最后一行code_generation(0, 30)的两个参数的值，
     - 第一个值决定了纵向生成容器时两个元素相差多少会分到两个容器中，
     - 第二个值决定了横向生成容器时两个元素相差多少会分到两个容器中。
     - 代码运行时会先调用元素识别网络对输入图片进行预测，预测的结果会通过labelImg打开，并可以进行手动修改，修改后的文件保存到annotations中，
     - 关闭labelImg后会对每个元素进行样式推理，
     - 然后生成代码，生成的html代码保存在myhtml中，生成的css代码保存在mystyle.css中。

以下是本研究中使用的环境：

<img src="C:\Users\chenchen\AppData\Roaming\Typora\typora-user-images\image-20220611140837568.png" alt="image-20220611140837568" style="zoom: 50%;" />
