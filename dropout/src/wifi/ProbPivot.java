package wifi;

import com.aliyun.odps.udf.UDFException;
import com.aliyun.odps.udf.UDTF;
import com.aliyun.odps.udf.annotation.Resolve;

/**
 * ʹ��˵��:������prediction_detail��Ԥ����ʰ���չ��
 * �����ڶ�����Ԥ������(����mall_id)
 * ������Ϊһ�Զ��UDTF
 * ����:row_id,mall_id,prediction_detail
 * ���:row_id,mall_id,shop_code,prob
 */
@Resolve({"bigint,string,string->bigint,string,bigint,double"})
public class ProbPivot extends UDTF {

  @Override
  public void process(Object[] args) throws UDFException {
    Long row_id = (Long)args[0];
    String mall_id = (String)args[1];
    String prediction_detail = (String)args[2];
    prediction_detail=prediction_detail.substring(1,prediction_detail.length()-1);
    for (String i:prediction_detail.split(",")){
    	String shop_code=i.substring(i.indexOf("\"")+1,i.indexOf(":")-1);
    	String prob=i.substring(i.indexOf(":")+2);
    	forward(row_id,mall_id,Long.parseLong(shop_code),Double.parseDouble(prob));
    }
    

  }
}
