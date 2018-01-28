package wifi;

import com.aliyun.odps.OdpsException;
import com.aliyun.odps.data.TableInfo;
import com.aliyun.odps.mapred.JobClient;
import com.aliyun.odps.mapred.RunningJob;
import com.aliyun.odps.mapred.conf.JobConf;
import com.aliyun.odps.mapred.utils.InputUtils;
import com.aliyun.odps.mapred.utils.OutputUtils;
import com.aliyun.odps.mapred.utils.SchemaUtils;

public class WifiPositionCount {

/*
 * Usage: <inputTable> <col_key> <col_position> <col_count> <outputTable>
 * ���ڰ�˳��λ��ͳ��wifi���ֵ��ܴ����������λ��ָ���Ǵ�ǿ������ʮ��˳��λ��
 * ͳ��ʱ��ÿ��λ�ó���һ�Σ���������λ��Ҳ��һ��
 * col_key��ͳ��ʱ���������key�����ж��У������Ÿ���
 * col_position��λ�ñ�ǣ�1-10��ʮ��λ��
 * col_count���ڸ�λ�ó��ֵĴ���
 * ������: col_key,col_position,col_count
 * �����: col_key;λ��1-λ��10�ļ���(��10��)
 * �����÷��ɲμ�sql����
 */
    public static void main(String[] args) throws Exception {
    	
    	System.out.println("Usage: <inputTable> <col_key> <col_position> <col_count> <outputTable>");
    	
    	JobConf job = new JobConf();
    	String[] col_key=args[1].split(",");
    	
    	//����������
        String[] input_cols=new String[col_key.length+2];
        for(int i=0;i<col_key.length;i++){
        	input_cols[i]=col_key[i];
        }
        input_cols[col_key.length]=args[2];
        input_cols[col_key.length+1]=args[3];
        
        
        //����MapOutputKeySchema
        StringBuilder MapOutputKeySchema=new StringBuilder();
        for(int i=0;i<col_key.length;i++){
        	MapOutputKeySchema.append(col_key[i]);
        	if (i==col_key.length-1){
        		MapOutputKeySchema.append(":string");
        	}else{
        		MapOutputKeySchema.append(":string,");
        	}
        }
        
        
        job.setMapperClass(WifiPositionCountMapper.class);
        job.setReducerClass(WifiPositionCountReducer.class);

        job.setMapOutputKeySchema(SchemaUtils.fromString(MapOutputKeySchema.toString()));
        job.setMapOutputValueSchema(SchemaUtils.fromString("position:bigint,count:bigint"));

        InputUtils.addTable(TableInfo.builder().tableName(args[0]).cols(input_cols).build(), job);
        OutputUtils.addTable(TableInfo.builder().tableName(args[4]).build(), job);

        JobClient.runJob(job);
      }

}
