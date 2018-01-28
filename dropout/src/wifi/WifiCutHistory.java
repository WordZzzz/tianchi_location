package wifi;

import java.util.HashSet;

import com.aliyun.odps.udf.UDFException;
import com.aliyun.odps.udf.UDTF;
import com.aliyun.odps.udf.annotation.Resolve;
/**
 * ʹ��˵��:������ÿ��row_id�е�wifi_info����չ��
 * ������user_shop_behavior��
 * ������Ϊһ�Զ��UDTF
 * ����:row_id,mall_id,shop_id,wifi_info
 * ���:row_id,mall_id,shop_id,wifi_id,db,flag
 */
@Resolve({"bigint,string,string,string->bigint,string,string,string,bigint,boolean"})
public class WifiCutHistory extends UDTF {
  @Override
  public void process(Object[] args) throws UDFException {
    Long row_id = (Long) args[0];
    String mall_id = (String) args[1];
    String shop_id = (String) args[2];
    String wifi_info = (String) args[3];
    HashSet<String> wifi_set = new HashSet<String>();
    for (String i:wifi_info.split(";")){
        String[] info = i.split("\\|");
        if (!wifi_set.contains(info[0])){
        	wifi_set.add(info[0]);
        	Long db = null;
        	try{
        		db = Long.parseLong(info[1]);
        	}catch(Exception e){}
        	forward(row_id,mall_id,shop_id,info[0],db,info[2].equals("true")?true:false);
    
        }
    }
  }
}
