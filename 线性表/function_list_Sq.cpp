#include <iostream>
#include <process.h>
#define LIST_INIT_SIZE 100
#define LIST_INCREASEMENT 10
using namespace std;
typedef int ElemType;
typedef struct
{
    ElemType *elem;
    int length;
    int init_size;
    int increasement;

} List_Sq;

// 初始顺序表
void InitList_Sq(List_Sq &L)
{
    L.elem = new ElemType[LIST_INIT_SIZE];
    L.length = 0;
    L.init_size = LIST_INIT_SIZE;
    L.increasement = LIST_INCREASEMENT;
}

// 销毁顺序表
void DestoryList_Sq(List_Sq &L)
{
    delete[] L.elem;
    L.init_size = 0;
    L.length = 0;
    cout << "顺序表已销毁！！！" << endl;
}

// 重置空表
void ClearList(List_Sq &L)
{
    if (L.length > 0)
    {
        L.length = 0;
        cout << "线性表已经重置为空表！" << endl;
    }
    else
        cout << "线性表不存在，无法重置为空表！" << endl;
}

// 判断是否为空表
bool ListEmpty(List_Sq &L)
{
    if (L.length == 0)
        return true;
    else if (L.length != 0)
        return false;
}

// 求线性表长度
int ListLength(List_Sq &L)
{
    return L.length;
}

// 查找顺序表元素
ElemType GetElem(List_Sq &L, int i, ElemType e)
{
    if (i < 1 || i > L.length)
    {
        cout << "i的值不合法,超出了线性表范围" << endl;
        exit(1);
    }
    else
    {
        e = L.elem[i - 1];
        return e;
    }
}

// 返回顺序表元素位序
int LocateElem(List_Sq &L, ElemType e)
{
    ElemType *p;
    p = L.elem;
    int i = 1;
    while (i <= L.length && *p++ != e)
        ++i;
    if (i > L.length)
        return 0;
    else
        return i;
}

// 返回元素前驱
ElemType PriorElem(List_Sq &L, ElemType cur_e, ElemType &pre_e)
{
    int i = 0;
    while (L.elem[i] != cur_e)
    {
        i++;
    }
    if (i == 0)
    {
        cout << "元素cur_e是第一个元素,没有前驱!" << endl;
        exit(1);
    }
    pre_e = L.elem[i - 1];
    return pre_e;
}

// 返回元素后继
ElemType NextElem(List_Sq &L, ElemType cur_e, ElemType &next_e)
{
    int i = 0;
    while (L.elem[i] != cur_e)
    {
        i++;
    }
    if (i == L.length - 1)
    {
        cout << "元素cur_e是最后一个元素,没有后继!" << endl;
        exit(1);
    }
    next_e = L.elem[i + 1];
    return next_e;
}

ElemType *a;
// 定义增量函数
void Increasement_Sq(List_Sq &L)
{

    a = new ElemType[L.init_size + L.increasement];
    for (int i = 0; i < L.length; i++)
        a[i] = L.elem[i];
    delete[] L.elem;
    L.elem = a;
    L.init_size += L.increasement;
}
// 错误指示函数
void Errormessage(char *s)
{
    cout << s << endl;
    exit(1);
}
// 插入顺序表元素
void ListInsert(List_Sq &L, int i, ElemType e)
{
    if (i < 1 || i > L.length + 1)
        Errormessage("i的值不合法");
    if (L.length >= L.init_size)
        Increasement_Sq(L);
    ElemType *q, *p;
    q = &(L.elem[i - 1]);
    for (p = &L.elem[L.length - 1]; p >= q; --p)
        *(p + 1) = *p;
    *q = e;
    L.length++;
}

// 删除顺序表元素
void ListDelete(List_Sq &L, int i, ElemType &e)
{
    if (i < 1 || i > L.length)
        Errormessage("i的值不合法");
    ElemType *q, *p;
    q = &(L.elem[i - 1]);
    e = *q;
    q = &(L.elem[L.length - 1]);
    for (p = &L.elem[i]; p <= q; ++p)
        *(p - 1) = *p;
    L.length--;
    cout << "删除的元素为:" << e << endl;
}

// 依次输出L每个数据元素
void ListTraverse(List_Sq &L)
{
    int i = 0;
    cout << "<";
    while (i < L.length - 1)
    {
        cout << L.elem[i] << " ";
        i++;
    }
    cout << L.elem[i] <<" >"<<endl;
}

void putp(List_Sq &L)
{
    char ch;
    int c = 1;
    cout << "请输入需要的顺序表元素:" << endl;
    while ((ch = getchar()) != '\n')
    {
        if (ch == ' ')      continue;
        ListInsert(L, c, int(ch - '0'));
        c++;
    }
}
// A和B交集
List_Sq Intersection_List_Sq(List_Sq &LA, List_Sq &LB)
{
    List_Sq LC;
    InitList_Sq(LC);
    for (int i = 0; i <= LA.length - 1; i++)
        for (int j = 0; j <= LB.length - 1; j++)
            if (LA.elem[i] == LB.elem[j])
                LC.elem[LC.length++] = LA.elem[i];
    cout << "A * B = ";
    return LC;
}
//A和B并集
List_Sq addictation_List_Sq(List_Sq &LA, List_Sq &LB)
{
    List_Sq LD;
    InitList_Sq(LD);
    for (int i = 0; i <=LA.length-1; i++)
        LD.elem[LD.length++] = LA.elem[i];
    int k = LD.length - 1;
    for (int i = 0; i <= LB.length - 1; i++)
    {
        bool cmp = 0;
        for (int j = 0; j <= k; j++)
            if (LD.elem[j] == LB.elem[i])
                {
                cmp = 1;
                break;
                }
        if(!cmp)LD.elem[LD.length++] = LB.elem[i];
    }
    cout << "A U B = ";
    return LD;
}
// A和B差集 A-B
List_Sq subtraction_List_Sq(List_Sq &LA, List_Sq &LB)
{
    List_Sq LC;
    InitList_Sq(LC);
    for (int i = 0; i <= LA.length - 1; i++){
        bool cmp = 0;
        for (int j = 0; j <= LB.length - 1; j++)
            if(LA.elem[i]==LB.elem[j]){
                cmp = 1;
                break;
            }
        if(!cmp){
            LC.elem[LC.length++] = LA.elem[i];
        }
    }     

    return LC;
}
//格式化输入
void putq(List_Sq &L)
{
    InitList_Sq(L);
    int n,m;
    cout << "num = ";
    cin >> n;
    cout << "elem = ";
    for (int i = 0; i < n; i++)
    {
       
        cin >> m;
        L.elem[L.length++] = m;
    }
}