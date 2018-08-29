
-- ---- 0 文件导入导出



-- ----  1 数据库
DROP DATABASE IF EXISTS hive_sql;  -- 如果存在，删除数据库
CREATE DATABASE hive_sql           -- 新建数据库，添加注释、存储位置
  COMMENT 'HQL使用'
  LOCATION 'hdfs://nameservice1/inceptor1/user/hive/warehouse';
-- ALTER DATABASE hive_sql SET OWNER user_or_role; -- 修改用户
-- ALTER DATABASE hive_sql SET LOCATION 'hdfs://nameservice1/inceptor1/user/hive';  -- 修改存储路径

SHOW DATABASES;
USE hive_sql;
-- use defualt;

-- ----  2 建表与删表
-- TRUNCATE TABLE table_name [PARTITION partition_spec];
drop table if exists hive_sql_table;
CREATE TABLE hive_sql_table(
	company_name STRING NOT NULL PRIMARY KEY COMMENT '公司名',  -- 字段名、数据类型、默认非空、主键、字段注释
	chanle_id STRING NOT NULL COMMENT '公司ID',
	company_gather_time STRING DEFAULT NULL COMMENT '采集时间',
	count NUMBER DEFAULT 1 COMMENT '计数',    --  默认值 1
	CONSTRAINT for_foreign FOREIGN KEY (chanle_id) REFERENCES company_base_contact_info(chanle_id))  -- 外键
COMMENT '公司基本信息表'    -- 表注释
PARTITIONED BY(today STRING, country STRING)  -- 分区
row format delimited  
	fields terminated by ','    -- 指定导入数据的列与列之间的分隔符
	collection ITEMS TERMINATED BY  '-'    -- 指定Array类型的分隔符
	map keys terminated by ':'     -- 指定map类型的分隔符
	lines terminated by '\n'    -- 指定行与行之间的分隔符
LOCATION 'hdfs://nameservice1/inceptor1/user/hive/warehouse/hive_sql_table';  -- 存储路径

-- 复制表结构
CREATE TABLE company_base_contact_info
	LIKE data_hub_new.company_base_contact_info_new;
INSERT INTO TABLE company_base_contact_info 
	select * 
	FROM data_hub_new.company_base_contact_info_new;

-- 复制表结构及其数据
create table `company_base_contact_info` 
	AS
	select 
	chanle_id, 
	company_name, 
	company_gather_time 
	from data_hub_new.company_base_contact_info_new ;

-- 外部表
CREATE EXTERNAL TABLE hive_sql_table_1(
	viewTime INT, 
	country STRING COMMENT 'country of origination')
	COMMENT 'This is the staging page view table'
	ROW FORMAT DELIMITED FIELDS TERMINATED BY '\054'
	STORED AS TEXTFILE   -- 纯文本文件，文件存储形式，如果数据需要压缩，使用 STORED AS SEQUENCE 。
	LOCATION 'hdfs://nameservice1/inceptor1/user/hive/warehouse/hive_sql_table_1';

-- 分区
-- 分区表使得查询时指定分区而不必查询整个表，节约时间
-- 分区表的字段在整个表里其实就是一个普通的字段,每个分区以文件夹的形式单独存在表文件夹的目录下
create external table table_name(
	filed STRING) PARTITIONED BY (partition_field NUMBER) -- 建（映射表)分区
ROW FORMAT DELIMITED 
	FIELDS TERMINATED BY '\t' 
stored as textfile
location '\tmp';

alter table table_name 
	add IF NOT EXISTS partition(partition_field='part') -- 添加数据到分区
	location '\tmp';

ALTER TABLE table_name DROP part ; -- 删除分区

load data local inpath '/home/hadoop/Desktop/data.txt' 
	overwrite into table rable_name partition (ds='2015-11-11'); -- 将本地数据添加到分区中

insert overwrite table table_name 
	partition (ds='**') select id,max(name) from test group by id; -- 往一个分区表的某个分区中添加数据

select * 
	from table_name 
	where partition_field ='**';  -- 分区中查询

-- ----  3 修改表
ALTER TABLE hive_sql_table RENAME TO hive_sql_rename;  -- 修改表名
-- ALTER TABLE table_name SET TBLPROPERTIES table_properties;
ALTER TABLE hive_sql_rename SET TBLPROPERTIES('comment' = '修改后的表名');

-- 改变列名、数据类型、注释、列位置或者它们的任意组合
ALTER TABLE hive_sql_rename CHANGE company_name company_n STRING AFTER chanle_id;  -- 修改列名，并放在chanle_id后面
ALTER TABLE hive_sql_rename CHANGE company_name company_n STRING FIRST;  -- 修改列名，并放在首列
alter table odm_company_base_business_merge CHANGE COLUMN company_name company_name STRING comment '公司名';  -- 修改字段注释

-- ADD是代表新增一字段，字段位置在所有列后面(partition列前)
ALTER TABLE hive_sql_rename ADD COLUMNS (company_email INT COMMENT '公司邮箱');
-- REPLACE则是表示替换表中所有字段
ALTER TABLE hive_sql_rename REPLACE COLUMNS (company_telephone INT COMMENT '公司邮箱');

-- 删除列
ALTER TABLE hive_sql_rename DROP company_name;

-- ----  4 视图
-- 视图是只读的，不能用LOAD/INSERT/ALTER
DROP VIEW IF EXISTS hive_view;
CREATE VIEW hive_view(
	company_name COMMENT '公司名')
	AS
	SELECT DISTINCT company_name
	FROM hive_sql_rename
	WHERE province = '山东' ;

-- ----  5 索引
DROP INDEX IF EXISTS index_name ON hive_sql_table;
-- CREATE INDEX index_name ON hive_sql_table(company_name);

-- ----  6 数据查询 select
SELECT * 
	FROM sales 
	WHERE amount > 10 AND region = "US";

SELECT DISTINCT col1, col2 FROM t1;

-- group by  having
SELECT col1 
	FROM t1 
	GROUP BY col1 
	HAVING SUM(col2) > 10;

-- ORDER BY 全局排序，只有一个Reduce任务
-- SORT BY 只在本机做排序
SELECT * 
	FROM customers 
	ORDER BY create_date 
	LIMIT 2,5;
-- Top k 查询: 查询销售记录最大的 5 个销售代表。
--SET mapred.reduce.tasks = 1;
SELECT * 
	FROM test 
	SORT BY amount 
	DESC LIMIT 5;

-- 正则表达式，下面的语句查询除了 ds 和 hr 之外的所有列：
SELECT `(ds|hr)?+.+` 
	FROM test;

-- IN, NOT IN     不支持EXIST ,NOT EXIST

-- join  偏于横向的联合
-- left outer join和right outer join
-- left outer join会把左边表的字段全部选择出来，右边表的字段把符合条件的也选择出来，不满足的全部置空，也就是说以左边表为参照
SELECT a.* 
	FROM a JOIN b 
	ON (a.id = b.id);

SELECT a.* 
	FROM a JOIN b 
	ON (a.id = b.id AND a.department = b.department);

SELECT a.val, b.val, c.val 
	FROM a JOIN b 
	ON (a.key = b.key1) 
	JOIN c 
	ON (c.key = b.key2);

-- HAVING Clause
SELECT col1 
	FROM t1 
	GROUP BY col1 
	HAVING SUM(col2) > 10

SELECT col1 
	FROM (SELECT col1, SUM(col2) AS col2sum 
			FROM t1 
			GROUP BY col1) t2 
	WHERE t2.col2sum > 10

-- union union all   两张表字段必须是相同的.合并数据条数，等于是纵向的
-- union如果存在相同的数据记录会被合并，而union all不会合并相同的数据记录，该有多少条记录就会有多少条记录
-- Applying Subclauses
SELECT key FROM (SELECT key FROM src ORDER BY key LIMIT 10)subq1
UNION
SELECT key FROM (SELECT key FROM src1 ORDER BY key LIMIT 10)subq2;

-- Column Aliases for Schema Matching
INSERT OVERWRITE TABLE target_table
  SELECT name, id, category FROM source_table_1
  UNION ALL
  SELECT name, id, "Category159" FROM source_table_2;

-- Column Type Conversion
SELECT name, id, cast('2001-01-01' as date) d FROM source_table_1
UNION ALL
SELECT name, id, hiredate as d FROM source_table_2;

-- case  when  else  end
SELECT 
	company_name,
	company_email,
	CASE 
		WHEN company_email = '暂无' THEN '未知'
		WHEN LENGTH(company_email) = 0 THEN '未知'
		ELSE company_email 
	END AS email
	FROM odm_1.odm_company_base_contact_info;

SELECT 'Number of Titles', Count(*) 
FROM titles 
GROUP BY 
    CASE 
        WHEN price IS NULL THEN 'Unpriced' 
        WHEN price < 10 THEN 'Bargain' 
        WHEN price BETWEEN 10 and 20 THEN 'Average' 
        ELSE 'Gift to impress relatives' 
    END  ;

-- 为了在 GROUP BY 块中使用 CASE，查询语句需要在 GROUP BY 块中重复 SELECT 块中的 CASE 块
SELECT 
	Title， 
    CASE 
        WHEN price IS NULL THEN 'Unpriced' 
        WHEN price < 10 THEN 'Bargain' 
        WHEN price BETWEEN 10 and 20 THEN 'Average' 
        ELSE 'Gift to impress relatives' 
    END AS Range,      
FROM titles 
GROUP BY 
    CASE 
        WHEN price IS NULL THEN 'Unpriced' 
        WHEN price < 10 THEN 'Bargain' 
        WHEN price BETWEEN 10 and 20 THEN 'Average' 
        ELSE 'Gift to impress relatives' 
    END, 
     Title 
ORDER BY 
    CASE 
        WHEN price IS NULL THEN 'Unpriced' 
        WHEN price < 10 THEN 'Bargain' 
        WHEN price BETWEEN 10 and 20 THEN 'Average' 
        ELSE 'Gift to impress relatives' 
    END, 
     Title ;

-- like 与  Not like 
-- like不是正则，而是通配符。这个通配符可以看一下SQL的标准，例如%代表任意多个字符。
-- 像mysql中的"like",%代表任意数量个字符，_代表一个填充字符。但是建议使用高级函数"instr"效率更高。
select "aaaaa" like "%aaa%" from test_struct limit 10;
Select dataforjy  
	from fdm_dm.dmp_plsadm_tradeinfo_m_20180227_mix
	where dataforjy like '%#____'
	   or dataforjy like '%_#___'
	   or dataforjy like '%__#__'
	   or dataforjy like '%___#_'
	   or dataforjy like '%____#';
-- Not like 表示不包含的匹配，和like相反，但是用法不是Anot like B，而是not A like B 
select  not 'abcde' like '%c%e'      
	from  fdm_dm.dmp_plsadm_tradeinfo_m_20180227_mix;

-- rlike 与  not rlike
-- rlike是正则，正则的写法与java一样。'\'需要使用'\\',例如'\w'需要使用'\\w'
select "aaaaa" rlike "%aaa%" from test_struct limit 10;
select 1 
	from lxw_dual 
	where 'footbar' 
	rlike'^f.*r$';
select 1 
	from lxw_dual 
	where '123456' 
	rlike'^\\d+$';  -- 判断一个字符串是否全为数字
Select  dataforjy
	from fdm_dm.dmp_plsadm_tradeinfo_m_20180227_mix
	where substr(dataforjy,length(dataforjy)-4)  -- substr后5位的取法，是dataforjy-4,而不是dataforjy-5
	rlike '#';
-- 其实dataforjy like ‘%#%’和dataforjyr like ‘#’效果一样，都是对含#号的匹配。
-- 但是上面两种如果dataforjy字段中存在长度小于5的字段，则统计结果都会不准。
-- NOT RLIKE 的使用，也是NOT A RLIKEB
select  PAYSTAT24MONTH
	from  fdm_dm.dmp_plsadm_tradeinfo_m_20180227_mix
	where not substr(PAYSTAT24MONTH,length(PAYSTAT24MONTH)-4) 
	rlike '#';

-- regexp_extract()   正则表达式提取数据的函数，
-- regexp_extract(string subject, string pattern, int index)
-- 通过下标返回正则表达式指定的部分。regexp_extract(‘foothebar’, ‘foo(.*?)(bar)’, 2) returns ‘bar.’
-- 注意，这里的index指的是：返回所有匹配的第N个。只有当匹配成功的对象>=2的时候，index可以选1,2。一般情况下是0.
select uid,  
      visittime,  
      pageUrl,  
      r_id,  
      regexp_extract(pageUrl,'(?<=p-)\\d+(?=\\.html)',0) as pid  --根据URL提取产品ID的使用
from sitevisitlog  
where statdate='20141021'  ;
