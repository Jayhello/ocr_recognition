package com.recognition;

import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.text.DecimalFormat;

import net.sourceforge.tess4j.*;
import org.bytedeco.javacpp.opencv_core.Mat;
import org.bytedeco.javacpp.opencv_core.Rect;

import static cv.skindetect.CvConvertHelper.matToImg;

/**
 * Created by DW_xiongyu on 2016/11/21.
 */
public class TesseractExample {

    public static String getRectWord(BufferedImage img, Rect rect) throws TesseractException {

        ITesseract instance = new Tesseract();  // JNA Interface Mapping
        String fontPath = "E:/char_recongition/Tesseract-OCR/tessdata";
        instance.setDatapath(fontPath);
        instance.setLanguage("chi_sim");

        long start = System.currentTimeMillis();
        Rectangle rectangle = new Rectangle(rect.x(), rect.y(), rect.width(), rect.height());
        String result = instance.doOCR(img, rectangle);
        long end = System.currentTimeMillis();


        DecimalFormat form = new DecimalFormat("0.00");
        //float xRatio = (float)rect.width() / img.getWidth();
        //float yRatio = (float)rect.height() / img.getHeight();
        //String strRatio = " xRatio " + form.format(xRatio) + " yRatio :" + form.format(yRatio);

        System.out.println(" result: " + result+" time consume :"+(float)(end-start)/1000 + "S");

        return result;
    }

    public static void main(String[] args) {
        String path = "F:/img_test/online_sample_img/10.jpg";


        File imageFile = new File(path);
        ITesseract instance = new Tesseract();  // JNA Interface Mapping

        try {
            String fontPath = "E:/char_recongition/Tesseract-OCR/tessdata";
            instance.setDatapath(fontPath);

            instance.setLanguage("chi_sim");

            long start = System.currentTimeMillis();
            String result = instance.doOCR(imageFile);
            long end = System.currentTimeMillis();
            System.out.println("Tesseract time consume :"+(float)(end-start)/1000 + "S");
            System.out.println(result);
        } catch (TesseractException e) {
            System.err.println(e.getMessage());
        }
    }
}
