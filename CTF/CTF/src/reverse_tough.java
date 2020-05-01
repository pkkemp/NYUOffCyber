import java.util.HashMap;
import java.util.Scanner;

public class reverse_tough
{
    public static int[] realflag = {9,4,23,8,17,1,18,0,13,7,2,20,16,10,22,12,19,6,15,21,3,14,5,11};
    public static int[] therealflag = {20,16,12,9,6,15,21,3,18,0,13,7,1,4,23,8,17,2,10,22,19,11,14,5};
    public static HashMap<Integer, Character> theflags = new HashMap<>();
    public static HashMap<Integer, Character> theflags0 = new HashMap<>();
    public static HashMap<Integer, Character> theflags1 = new HashMap<>();
    public static HashMap<Integer, Character> theflags2 = new HashMap<>();
    public static boolean m = true;
    public static boolean g = false;
    
    public static void main(String args[]) {
        check();
    }
    public static boolean check(){

        String originalFlag = "\u009D\u009DíÓÚ¢Ö¦¥Î\u0091f\u008FÇ¦á«ÀÖÑÎ«¥Ó";
        //String originalFlag = "ì¨ ¢«¢¥Ç©© ÂëÏãÒËãhÔÊ";
        for(int p = 0; p < originalFlag.length(); p++){
            if(true){
                originalFlag = originalFlag.substring(0,p) + (char)((int)(originalFlag.charAt(p)-10)) + originalFlag.substring(p+1);
            }
        }
        return true;
    }

}
