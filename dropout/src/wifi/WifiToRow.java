package wifi;

import com.aliyun.odps.OdpsException;
import com.aliyun.odps.data.TableInfo;
import com.aliyun.odps.mapred.JobClient;
import com.aliyun.odps.mapred.RunningJob;
import com.aliyun.odps.mapred.conf.JobConf;
import com.aliyun.odps.mapred.utils.InputUtils;
import com.aliyun.odps.mapred.utils.OutputUtils;
import com.aliyun.odps.mapred.utils.SchemaUtils;

public class WifiToRow {

/*
 * Usage: <inputTable> <outputTable>
 * ���ڽ�ÿ����¼(��row_idΪ����)չ����wifi_info���ºϲ���һ�У���23��
 * ����:row_id,mall_id,db_rank,wifi_id,db,flag
 * ���: 
 * ��1��:row_id
 * ��2��:mall_id
 * ��3-12��:��ǿ���������wifi_id
 * ��13-22��:3-12��wifi_id��Ӧ��wifiǿ��
 * ��23��:���ӵ�wifi_id
 */
    public static void main(String[] args) throws Exception {
    	
    	System.out.println("Usage: <inputTable> <outputTable>");
    	JobConf job = new JobConf();
        
        job.setMapperClass(WifiToRowMapper.class);
        job.setReducerClass(WifiToRowReducer.class);

        job.setMapOutputKeySchema(SchemaUtils.fromString("row_id:bigint,mall_id:string"));
        job.setMapOutputValueSchema(SchemaUtils.fromString("position:bigint,wifi_id:string,db:bigint,flag:boolean"));

        InputUtils.addTable(TableInfo.builder().tableName(args[0]).cols(new String[]{"row_id","mall_id","db_rank","wifi_id","db","flag"}).build(),job);
        OutputUtils.addTable(TableInfo.builder().tableName(args[1]).build(),job);

        JobClient.runJob(job);
      }

}
