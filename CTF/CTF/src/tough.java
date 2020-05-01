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
        //deMap();
        printflags();
        String userInput = "rtcp{owr3w_4_4_h4cakr_y0u_4o3}";
        brute("ì¨ ¢«¢¥Ç©© ÂëÏãÒËãhÔÊ".length());
        //userInput = "rtcp{h3r3s_a_fr33_fl4g!}";
        String input = userInput.substring("rtcp{".length(),userInput.length()-1);
        if (check(input)) {
            System.out.println("Access granted.");
        } else {
            System.out.println("Access denied!");
        }
    }
    public static void printflags() {
        String tempstring = "";
        for(int i = 0; i < realflag.length; i++) {
            tempstring += (char)realflag[i];
        }
        System.out.println(tempstring);
        tempstring = "";
        for(int i = 0; i < therealflag.length; i++) {
            tempstring += (char)realflag[i];
        }
        System.out.println(tempstring);

    }
    public static void deMap(){
        String flag = "ì¨ ¢«¢¥Ç©© ÂëÏãÒËãhÔÊ";
        String comp = " áÓÚ¢ðÇ¥Îg¢¦¢ÚÖ¾£hêÖ";
        // Creating array of string length
//        for(int p = 0; p < flag.length(); p++){
//            if((int)(flag.charAt(p)) > 156 && (int)(flag.charAt(p)) < 167){
//                flag = flag.substring(0,p) + (char)((int)(flag.charAt(p)-10)) + flag.substring(p+1);
//            }
//        }
        char[] ch = new char[flag.length()];

        // Copy character by character into array
        for (int i = 0; i < flag.length(); i++) {

            ch[i] = flag.charAt(i);
            if (flag.charAt(i)>156 && flag.charAt(i)<167)
            {
                //ch[i] = (char) (flag.charAt(i)-10);
            }
        }
        System.out.println(flag);

    }

    public static String brute(int length) {
        String theFlag;
        String startFlag = "owr3w_4_4_h4cakr_y0u_4o3";
        char[] flag = new char[length];
        for (int i = 0; i < length; i++) {
            for(int j = 0; j < 4096; j++) {
                flag[i] = (char)j;
                String strFlag = new String(flag);
                try {
                    if(checkTest(strFlag).charAt(i) == flag[i]) {
                        break;
                    }
                } catch(NullPointerException e) {
                    continue;
                }

            }
        }
        theFlag = new String(flag);
        System.out.print(theFlag);
        return theFlag;
    }

    public static String checkTest(String input){
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
            return null;
        }
        if(input.charAt(input.length()-2) != 'o'){
            return null;
        }
        if(!input.substring(2,4).equals("r3") || input.charAt(5) != '_' || input.charAt(7) != '_'){
            return null;
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

        return thefinalflag;//.equals("ì¨ ¢«¢¥Ç©© ÂëÏãÒËãhÔÊ");
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
}
