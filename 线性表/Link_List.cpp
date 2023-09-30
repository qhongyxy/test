#include <iostream>
#define N 10000
using namespace std;
typedef int ElemType;
typedef struct LNode
{
    ElemType data;
    struct LNode *next;

} LNode, *LinkList;
// 输入
void putp(LinkList &L)
{
    L = NULL;
    LNode *s;
    cout << "请输入需要的单链表元素的个数:" << endl;
    int n, f[N];
    cin >> n;
    cout << "请输入需要的单链表元素:" << endl;
    for (int i = 1; i <= n; i++)
        cin >> f[i];
    cout << "输入完毕！" << endl;
    for (int i = n; i >= 1; i--)
    {
        s = new LNode;
        s->data = f[i];
        s->next = L;
        L = s;
    }
}
// 前插p结点
void ListInsert_L(LinkList &L, LNode *p, LNode *s)
{
    if (p == L)
    {
        s->next = p;
        L = s;
    }
    else
    {
        LNode *q;
        q = L;
        while (q->next && q->next != p)
            q = q->next;
        q->next = s;
        s->next = p;
    }
}
// 后插p结点
void ListInsert_N(LinkList &L, LNode *p, LNode *s)
{
    s->next = p->next;
    p->next = s;
}
// 求单链表长度
int List_Length(LinkList &L)
{
    LNode *p;
    int k = 0;
    p = L;
    while (p)
    {
        k++;
        p = p->next;
    }
    return k;
}
// 删除单链表结点
ElemType Delete_LinkList(LinkList &L, LNode *p, ElemType &e)
{
    if (p == L)
        L = p->next;
    else
    {
        LNode *q;
        q = L;
        while (q->next && q->next != p)
            q = q->next;
        q->next = p->next;
    }
    e = p->data;
    delete p;
    return e;
}
// 返回查找数据的指针
LNode *locate_LinkList(LinkList &L, ElemType &e)
{
    LNode *q;
    q = L;
    while (q && q->data != e)
        q = q->next;
    return q;
}
// 依次输出L每个数据元素
void Traverse_ListLink(LinkList &L)
{
    cout << "<";
    LNode *p;
    p = L;
    while (p->next)
    {
        cout << p->data << " ";
        p = p->next;
    }
    cout << p->data << " >" << endl;
}

// 销毁顺序表
void Destory_ListLink(LinkList &L)
{
    LNode *p;
    while (L)
    {
        p = L;
        L = L->next;
        delete p;
    }

    cout << "顺序表已销毁！！！" << endl;
}

// 重置空表
void Clear_ListLink(LinkList &L)
{
    LNode *p;
    while (L->next)
    {
        p = L->next;
        L->next = p->next;
        delete p;
    }
}

// 判断是否为空表
bool Empty_ListLink(LinkList &L)
{
    if (L->next == NULL)
        return true;
    else
        return false;
}

// 返回顺序表元素位序
int Locate_ListLink(LinkList &L, ElemType e)
{
    LNode *p;
    p = L;
    int i = 1;
    while (p->data != e)
    {
        ++i;
        p = p->next;
    }

    if (i > List_Length(L))
        return 0;
    else
        return i;
}

// 返回元素前驱
LNode *Prior_ListLink(LinkList &L, LNode *p)
{
    int i = 0;
    LNode *q;
    q = L;
    while (q->next && q->next != p)
    {
        q = q->next;
        i++;
    }
    if (i == 0)
    {
        cout << "元素cur_e是第一个元素,没有前驱!" << endl;
        exit(1);
    }
    return q;
}

// 返回元素后驱
LNode *Last_ListLink(LinkList &L, LNode *p)
{
    int i = 0;
    LNode *q;
    q = L;
    while (q && q != p)
    {
        q = q->next;
        i++;
    }
    if (i >= List_Length(L))
    {
        cout << "元素cur_e是最后一个元素,没有后驱!" << endl;
        exit(1);
    }
    q = q->next;
    return q;
}
//逆置链表
 void invert_ListLink(LinkList &L){
    LNode *p, *s;
    p = L;
    L = NULL;
    while(p){
        s = p;
        p = p->next;
        s->next = L;
        L = s;
    }
 }
// // 求两单链表的差集 eg:A-B
// LinkList subtraction_LinkList(LinkList &LA, LinkList &LB)
// {
//     LNode *p, *q, *v;
//     p = LA, q = LB;
//     v = LB;
//     while (p->next)
//     {
//         p = LA, q = LB;
//         v = LB;
//         int i = 0;
//         while (q->next)
//         {
//             if (p->data == q->data)
//             {
//                 if (i == 0)
//                 {
//                     LA = p->next;
//                     LB = q->next;
//                     delete p, q;
//                     break;
//                 }
//                 else
//                 {
//                     LA = p->next;
//                     v->next = q->next;
//                     delete p, q;
//                     break;
//                 }
//             }
//             else
//             {
//                 if (i > 0)
//                     v = v->next;
//                 q = q->next;
//             }
//             i++;
//         }
//     }
//     cout << "A-B的差集:" << endl;
//     return LA;
// }


//求两单链表的差集 eg:A-B,数组方法
LinkList subtraction_LinkList_shuzu(LinkList &LA, LinkList &LB)
{
    LinkList LD;
    LNode *p, *q, *w;
    p = LA, q = LB; 
    LD= NULL;
    w = LD;
    
    int A[N], B[N],C[N], i = 0, j = 0,k=0,cmp=0;
    while (p)
    {
        ++i;
        A[i] = p->data;
        p = p->next;
        
    }
    while (q)
    {
        ++j;
        B[j] = q->data;
        q = q->next;
    }
    for (int m = 1; m <= i; m++){
        cmp = 0;
        for (int n = 1; n <= j; n++)
            if (A[m] == B[n]){
                B[n] = 1e9;
                cmp = 1;
            }      
        if(cmp)
        A[m] = 1e9;
    }
    for (int m = 1; m <= i; m++)
      if(A[m]!=1e9)
            C[++k] = A[m];
    for (int m = 1; m <= k; m++)
        cout << C[m] << " ";
    cout << endl;
    for (int n = k; n >= 1; n--)
    {
         cout << C[n] << " ";
        w = new LNode;
        w->data = C[n];
        w->next = LD;
        LD = w;
    }
     cout << "A-B的差集:" << endl;
     return LD;
}
//A-B,链表做法
LinkList subtraction_LinkList(LinkList &LA, LinkList &LB)
{
     LinkList LD;
     LD = NULL;
     LNode *p, *q, *w;
     p = LA, q = LB, w = LD;
     while (p)
     {
        int cmp = 0;
        q = LB;
        while (q)
    {
        if(p->data==q->data){
                cmp = 1;
                break;
        }
        q = q->next;
    }
     if(!cmp){
        w = new LNode;
        w->data =p->data;
        w->next = LD;
        LD = w;
     }
     p = p->next;
    }
    invert_ListLink(LD);
     return LD;
}
// 求两单链表的合集 eg:A+B
LinkList and_LinkList_shuzu(LinkList &LA, LinkList &LB)
{
    LinkList LC;
    LNode *p, *q, *v;
    p = LA, q = LB;
    v = LC;
    LC = NULL;
    int A[N], B[N], i = 0, j = 0;
    while (p)
    {
        ++i;
        A[i] = p->data;
        p = p->next;
        
    }
    while (q)
    {
        ++j;
        B[j] = q->data;
        q = q->next;
    }
    for (int m = 1; m <= i; m++)
        for (int n = 1; n <= j; n++)
            if (A[m] == B[n])
                B[n] = 1e9;
    for (int m = 1; m <= j; m++)
        if (B[m] != 1e9)
            A[++i] = B[m];
    for (int n = i; n >= 1; n--)
    {
        v = new LNode;
        v->data = A[n];
        v->next = LC;
        LC = v;
    }
    cout << "A+B的合集:" << endl;
    return LC;
}
//A+B,链表做法
LinkList and_LinkList(LinkList &LA, LinkList &LB)
{
    LinkList LD;
    LD = NULL;
    LNode *p, *q, *w;
    p = LA, q = LB,w = LD;
    while(p){
         w = new LNode;
        w->data =p->data;
        w->next = LD;
        LD = w;
        p = p->next;
    }
   
    while (q)
    {
        int cmp = 0; 
        p = LA;
        while (p)
    {
        if(p->data==q->data){
                cmp = 1;
                break;
        }
        p= p->next;
    }
     if(!cmp){
        w = new LNode;
        w->data =q->data;
        w->next = LD;
        LD = w;
     }
     q = q->next;
    }
     cout << "A U B = ";
     invert_ListLink(LD);
     return LD;
}
//A*B,链表做法
LinkList Intersection_LinkList(LinkList &LA, LinkList &LB)
{
    LinkList LD;
    LD = NULL;
    LNode *p, *q, *w;
    p = LA, q = LB,w = LD;
    while (p)
    {
     q = LB;
     while (q)
     {
        if(p->data==q->data){
            w = new LNode;
        w->data =p->data;
        w->next = LD;
        LD = w;
        break;
        }
        q = q->next;
    }
       p= p->next;
    }
     cout << "A * B = " ;
     invert_ListLink(LD);
     return LD;
}
//格式化输出
void putq(LinkList &L)
{
    L = NULL;
    LNode *s;
    cout << "num = ";
    int n, f[N];
    cin >> n;
    cout << "elem = ";
    for (int i = 1; i <= n; i++)
        cin >> f[i];
    for (int i = n; i >= 1; i--)
    {
        s = new LNode;
        s->data = f[i];
        s->next = L;
        L = s;
    }
}