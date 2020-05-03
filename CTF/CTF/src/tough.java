import java.util.*;

public class tough
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
        Scanner scanner = new Scanner(System.in);
        //System.out.print("Enter flag: ");
        //String userInput = scanner.next();
        String flag = "ow0_wh4t_4_h4ckr_y0u_4r3";
        char[] decon = "ì¨ ¢«¢¥Ç©© ÂëÏãÒËãhÔÊ".toCharArray();
        char[] finalflag = "h3r3s_4_c0stly_fl4g_4you".toCharArray();
        String userInput = formatFlag(solveTough(flag));
        System.out.println(userInput);
        String input = userInput.substring("rtcp{".length(),userInput.length()-1);
        if (check(input)) {
            System.out.println("Access granted.");
        } else {
            System.out.println("Access denied!");
        }
    }

    public static boolean check(String input){
        boolean h = false;
        String flag = "ow0_wh4t_4_h4ckr_y0u_4r3";
        createMap(theflags, input, m);
        createMap(theflags0, flag, g);
        createMap(theflags1, input, g);
        createMap(theflags2, flag, m);
        String theflag = "";
        String thefinalflag = "";
        int i = 0;
        if(input.length() != flag.length()){
            return h;
        }
        if(input.charAt(input.length()-2) != 'o'){
            return false;
        }
        if(!input.substring(2,4).equals("r3") || input.charAt(5) != '_' || input.charAt(7) != '_'){
            return false;
        }
        //rtcp{h3r3s_a_fr33_fl4g!}
        for(; i < input.length()-3; i++){
            theflag += theflags.get(i);
        }
        for(; i < input.length();i++){
            theflag += theflags1.get(i);
        }
        for(int p = 0; p < theflag.length(); p++){
            thefinalflag += (char)((int)(theflags0.get(p)) + (int)(theflag.charAt(p)));
        }
        for(int p = 0; p < theflag.length(); p++){
            if((int)(thefinalflag.charAt(p)) > 146 && (int)(thefinalflag.charAt(p)) < 157){
                thefinalflag = thefinalflag.substring(0,p) + (char)((int)(thefinalflag.charAt(p)+10)) + thefinalflag.substring(p+1);
            }
        }

        return thefinalflag.equals("ì¨ ¢«¢¥Ç©© ÂëÏãÒËãhÔÊ");
    }
    public static void createMap(HashMap owo, String input, boolean uwu){
        if(uwu){
            for(int i = 0; i < input.length(); i++){
                owo.put(realflag[i],input.charAt(i));
            }
        } else{
            for(int i = 0; i < input.length(); i++){
                owo.put(therealflag[i],input.charAt(i));
            }
        }
    }

    public static String solveTough(String flag) {
        char[] flagToReverse = "ì¨ ¢«¢¥Ç©© ÂëÏãÒËãhÔÊ".toCharArray();
        String thefinalflag = "";
        createMap(theflags0, flag, g);
        createMap(theflags2, flag, m);
        char[] actualflag = new char[24];
        String theflag = "";

        for (int i = 0; i < flagToReverse.length; i++) {
            if (flagToReverse[i] > 156 && flagToReverse[i] < 167) {
                thefinalflag += (char)(flagToReverse[i]-10);
            } else {
                thefinalflag += (char)(flagToReverse[i]);
            }
        }
        for (int i = thefinalflag.length()-1; i >= 0; i--) {
            theflag = (char)(((int)thefinalflag.charAt(i))-((int)theflags0.get(i))) + theflag;
        }
        for (int i = theflag.length()-1; i >= theflag.length()-3; i--) {
            theflags1.put(i, theflag.charAt(i));
        }
        for (int i = theflag.length()-4; i >= 0; i--) {
            theflags.put(i, theflag.charAt(i));
        }
        for (int i = 0; i < theflag.length(); i++) {
            if (realflag[i] < 21) {
                actualflag[i] = theflags.get(realflag[i]);
            }
        }
        for (int i = 0; i < theflag.length(); i++) {
            if (therealflag[i] > 20) {
                actualflag[i] = theflags1.get(therealflag[i]);
            }
        }

        actualflag[2] = 'r';
        actualflag[3] = '3';
        actualflag[5] = '_';
        actualflag[7] = '_';
        actualflag[actualflag.length-2] = 'o';

        return (new String(actualflag));
    }
    public static String formatFlag(String flag) {
        return "rtcp{".concat(flag).concat("}");
    }

}
