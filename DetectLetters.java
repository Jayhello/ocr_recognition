package cv.wordExtract;

import com.recognition.TesseractExample;
import com.thrift.ocrimg.DetectLetter;
import net.sourceforge.tess4j.TesseractException;
import org.apache.commons.collections.CollectionUtils;
import org.bytedeco.javacpp.opencv_core.Point;
import org.bytedeco.javacpp.opencv_core.Scalar;
import org.bytedeco.javacpp.opencv_core.MatVector;
import org.bytedeco.javacpp.opencv_core.Size;
import org.bytedeco.javacpp.opencv_core.Mat;
import org.bytedeco.javacpp.opencv_core.Rect;
import org.junit.Test;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.LinkedList;
import java.util.List;

import static cv.skindetect.CvConvertHelper.imgToMat;
import static cv.skindetect.CvConvertHelper.matToImg;
import static org.bytedeco.javacpp.opencv_core.putText;
import static org.bytedeco.javacpp.opencv_core.FONT_HERSHEY_PLAIN;
import static org.bytedeco.javacpp.opencv_core.rectangle;
import static org.bytedeco.javacpp.opencv_highgui.*;
import static org.bytedeco.javacpp.opencv_imgproc.*;

/**
 * Created by DW_xiongyu on 2016/11/29.
 */
public class DetectLetters {

    //the minimum width and height of detected rect
    private final static int MIN_WH = 20;
    private final static int MINIMUM_AREA = 1000;
    private final static float HW_RATIO = 2.85F;
    //private final static double MINIMUM_AREA = 400;
    private final static int DETECT_COUNT_THREAD = 12;
    private final static boolean DEBUG = true;
    //private final static boolean DEBUG = false;
    private final static boolean SAVE = true;


    public List<Rect> getLetterRectLst(Mat srcMat, int i) throws IOException {
        List<Rect> rectList = new LinkedList<Rect>();

        Mat matGray = new Mat();
        cvtColor(srcMat, matGray, COLOR_RGB2GRAY);

        if (DEBUG) {
            imshow("matGray", matGray);
        }

        Mat matSobel = new Mat();
        Sobel(matGray, matSobel, 0, 1, 0, 3, 1, 0, BORDER_DEFAULT);
        if (DEBUG) {
            imshow("matSobel", matSobel);
        }


        Mat matThreshold = new Mat();
        threshold(matSobel, matThreshold, 0, 255, CV_THRESH_OTSU + CV_THRESH_BINARY);
        if (DEBUG) {
            imshow("matSobel2matThreshold", matThreshold);
        }

        Mat exElement = getStructuringElement(MORPH_RECT, new Size(17, 3));

        morphologyEx(matThreshold, matThreshold, CV_MOP_CLOSE, exElement);

        if(i > 0 && SAVE){
            String savePath = "F:/img_test/online_sample_img/extract_tmp/tmp/"+i+"mor.jpg";
            mat2ImgFile(matThreshold, savePath);
        }

        if (DEBUG) {
            imshow("matThreshold2morphologyEx", matThreshold);
        }
        //waitKey(0);

        MatVector matVector = new MatVector();
        findContours(matThreshold, matVector, RETR_EXTERNAL, CHAIN_APPROX_NONE);
        //findContours(matThreshold, matVector, RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);

        MatVector matVectorCopy = new MatVector(matVector.size());
        int len = (int) matVector.size();
        Mat matTmp;
        for ( i = 0; i < len; i++) {
            matTmp = matVector.get(i);
            approxPolyDP(matTmp, matVectorCopy.get(i), 3, true);
            Rect appRect = boundingRect(matVectorCopy.get(i));
            if (isWordRect(appRect)) {
                rectList.add(appRect);
                //System.out.println("nomal area: "+ appRect.area());
                //System.out.println("min area: "+ minAreaRect(matVectorCopy.get(i)).boundingRect().area());
            }
        }

        return rectList;
    }

    public void mat2ImgFile(Mat mat, String path) throws IOException {
        BufferedImage image  = matToImg(mat);
        ImageIO.write(image, "jpg", new File(path));
    }


    public void doExtract(String path) throws TesseractException, IOException {

        Mat imgMat = imread(path);
        System.out.println(" width: " + imgMat.cols() + " height: " + imgMat.rows());
        BufferedImage img = matToImg(imgMat);
        System.out.println(" width: " + img.getWidth()+ " height: " + img.getHeight());

        List<Rect> lstRect = getLetterRectLst(imgMat, -1);
        if (CollectionUtils.isNotEmpty(lstRect)){
            int count = 1;
            StringBuffer stringBuf = new StringBuffer();
            for (Rect rect:lstRect){
                rectangle(imgMat, rect, new Scalar(0, 255, 0, 0),  3, 8, 0);
                putText(imgMat, String.valueOf(count), new Point(rect.x(), rect.y()), FONT_HERSHEY_PLAIN, 2.8, new Scalar(0,0,0, 0));
                System.out.print("num: " + String.valueOf(count++) + " ");
                String str = TesseractExample.getRectWord(img, rect);
                stringBuf.append(str);
            }
            System.out.print("recognition result: " + stringBuf.toString().replaceAll("\n", ""));
        }

        imshow("imgMat", imgMat);
        waitKey(0);
        destroyAllWindows();
    }


    public static void main(String[] args) throws TesseractException, IOException {
        DetectLetters detectLetters = new DetectLetters();

        String path = "F:/huaya.jpg";
        path = "F:/img_test/online_sample_img/53.jpg";
        detectLetters.doExtract(path);
    }
}
