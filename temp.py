a = """  
    uid               
    name              
    url               
    created           
    updated           
    introduction      
    followers_count   
    question_count    
    avatar_url        
    best_answers_count
"""

print(a.split())

s = """
    id                 int auto_increment primary key,
    uid                varchar(64)  null comment '话题id',
    name               varchar(256) null comment '话题名称',
    url                varchar(256) null comment '话题url',
    created            timestamp    null comment '创建时间',
    updated            timestamp    null comment '更新时间',
    introduction       text         null comment '话题介绍',
    followers_count    int          null comment '关注数量',
    question_count     int          null comment '问题数量',
    avatar_url         varchar(256) null comment '话题头像',
    best_answers_count int          null comment '最佳回答数量'
"""

print([tuple(i.split())  for i in s.split(',')])



