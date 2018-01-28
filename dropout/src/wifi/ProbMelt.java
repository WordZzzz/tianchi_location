package wifi;

import com.aliyun.odps.udf.UDFException;
import com.aliyun.odps.udf.UDTF;
import com.aliyun.odps.udf.annotation.Resolve;

/**
 * ʹ��˵��:������prediction_detail�еĸ��ʰ���չ��
 * �������������͵�Ԥ������
 * ������Ϊһ�Զ��UDTF
 * ����:row_id,prediction_detail
 * ���:row_id,label,prob
 */
@Resolve({"bigint,string->bigint,string,double"})
public class ProbMelt extends UDTF {

  @Override
  public void process(Object[] args) throws UDFException {
    Long row_id = (Long)args[0];
    String prediction_detail = (String)args[1];
    prediction_detail=prediction_detail.substring(1,prediction_detail.length()-1);
    for (String i:prediction_detail.split(",")){
    	String shop_code=i.substring(i.indexOf("\"")+1,i.indexOf(":")-1);
    	String prob=i.substring(i.indexOf(":")+2);
    	forward(row_id,shop_code,Double.parseDouble(prob));
    }
    

  }
}
