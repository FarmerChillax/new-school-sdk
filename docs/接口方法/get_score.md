# 成绩接口

| 字段 | 默认值 | 类型 | 描述                   |
| ---- | ------ | ---- | ---------------------- |
| year | None   | int  | 查询学年               |
| term | 1      | int  | 查询学期，默认第一学期 |


## 示例
```py
from school_sdk.client import UserClient
from school_sdk import SchoolClient

# 实例化学校
Gdust = SchoolClient("172.16.254.1")

user:UserClient = Gdust.user_login("account", "password")

# 获取成绩, 2020-2021学年第一学期的成绩
score = user.get_score(year=2020, term=1)
print(score)
```

## 响应结果
```json
{
    "形势与政策Ⅴ": {
        "course_name": "形势与政策Ⅴ",
        "course_nature": "公共必修课",
        "course_target": "主修",
        "teacher": "徐丹丹",
        "exam_method": "考查",
        "exam_nature": "正常考试",
        "exam_result": "81",
        "credit": "0.3",
        "course_group": "马克思主义学院",
        "grade": "2018",
        "grade_point": "3.10"
    },
    "统一建模语言": {
        "course_name": "统一建模语言",
        "course_nature": "任选课",
        "course_target": "主修",
        "teacher": "侯爱民",
        "exam_method": "考查",
        "exam_nature": "正常考试",
        "exam_result": "89",
        "credit": "2.0",
        "course_group": "计算机学院",
        "grade": "2018",
        "grade_point": "3.90"
    },
    "Java Web课程设计": {
        "course_name": "Java Web课程设计",
        "course_nature": "专项实践课",
        "course_target": "主修",
        "teacher": "李玉坤",
        "exam_method": "考查",
        "exam_nature": "正常考试",
        "exam_result": "91",
        "credit": "2.0",
        "course_group": "计算机学院",
        "grade": "2018",
        "grade_point": "4.10"
    },
    "JavaScript课程设计": {
        "course_name": "JavaScript课程设计",
        "course_nature": "专项实践课",
        "course_target": "主修",
        "teacher": "王荣福",
        "exam_method": "考查",
        "exam_nature": "正常考试",
        "exam_result": "92",
        "credit": "2.0",
        "course_group": "计算机学院",
        "grade": "2018",
        "grade_point": "4.20"
    }
}
```

### 结果分析
```json
"<课程名>": {
    "course_name": "JavaScript课程设计", // 课程名
    "course_nature": "专项实践课",       // 课程属性
    "course_target": "主修",            // 课程性质
    "teacher": "王荣福",                // 授课老师
    "exam_method": "考查",              // 考核方式
    "exam_nature": "正常考试",
    "exam_result": "92",                // 考试成绩
    "credit": "2.0",                    // 学分 
    "course_group": "计算机学院",         // 课程归属学院
    "grade": "2018",                    // 学生年级
    "grade_point": "4.20"               // 绩点
}
```