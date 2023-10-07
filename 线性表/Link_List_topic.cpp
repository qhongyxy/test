#include <iostream>
#define N 10000
using namespace std;
typedef int ElemType;
typedef struct LNode
{
    ElemType data;
    struct LNode *next;

} LNode, *LinkList;
// ����
void putp(LinkList &L)
{
    L = NULL;
    LNode *s;
    cout << "��������Ҫ�ĵ�����Ԫ�صĸ���:" << endl;
    int n, f[N], m;
    cin >> n;
    cout << "��������Ҫ�ĵ�����Ԫ��:" << endl;
    for (int i = 1; i <= n; i++)
        cin >> f[i];
    cout << "������ϣ�" << endl;
    for (int i = n; i >= 0; i--)
    {
        s = new LNode;
        if(n>=1)
        s->data = f[i];
        s->next = L;
        L = s;
    }
}
// ǰ��p���
void ListInsert_L(LinkList &L, LNode *p, LNode *s)
{
    if (p == L->next)
    {
        s->next = p;
        L = s;
    }
    else
    {
        LNode *q;
        q = L->next;
        while (q->next && q->next != p)
            q = q->next;
        q->next = s;
        s->next = p;
    }
}
// ���p���
void ListInsert_N(LinkList &L, LNode *p, LNode *s)
{
    s->next = p->next;
    p->next = s;
}
// ��������
int List_Length(LinkList &L)
{
    LNode *p;
    int k = 0;
    p = L->next;
    while (p)
    {
        k++;
        p = p->next;
    }
    return k;
}
// ɾ����������
ElemType Delete_LinkList(LinkList &L, LNode *p, ElemType &e)
{
    if (p == L->next)
        L = p->next;
    else
    {
        LNode *q;
        q = L->next;
        while (q->next && q->next != p)
            q = q->next;
        q->next = p->next;
    }
    e = p->data;
    delete p;
    return e;
}
// ���ز������ݵ�ָ��
LNode *locate_LinkList(LinkList &L, ElemType &e)
{
    LNode *q;
    q = L->next;
    while (q && q->data != e)
        q = q->next;
    return q;
}
// �������Lÿ������Ԫ��
void Traverse_ListLink(LinkList &L)
{
    cout << "������ÿ������Ԫ��:" << endl;
    LNode *p;
    p = L->next;
    while (p->next)
    {
        cout << p->data << " ";
        p = p->next;
    }
    cout << p->data << endl;
}

// ����˳���
void Destory_ListLink(LinkList &L)
{
    LNode *p;
    while (L)
    {
        p = L;
        L = L->next;
        delete p;
    }

    cout << "˳��������٣�����" << endl;
}

// ���ÿձ�
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

// �ж��Ƿ�Ϊ�ձ�
bool Empty_ListLink(LinkList &L)
{
    if (L->next == NULL)
        return true;
    else
        return false;
}

// ����˳���Ԫ��λ��
int Locate_ListLink(LinkList &L, ElemType e)
{
    LNode *p;
    p = L->next;
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

// ����Ԫ��ǰ��
LNode *Prior_ListLink(LinkList &L, LNode *p)
{
    int i = 0;
    LNode *q;
    q = L->next;
    while (q->next && q->next != p)
    {
        q = q->next;
        i++;
    }
    if (i == 0)
    {
        cout << "Ԫ��cur_e�ǵ�һ��Ԫ��,û��ǰ��!" << endl;
        exit(1);
    }
    return q;
}

// ����Ԫ�غ���
LNode *Last_ListLink(LinkList &L, LNode *p)
{
    int i = 0;
    LNode *q;
    q = L->next;
    while (q && q != p)
    {
        q = q->next;
        i++;
    }
    if (i >= List_Length(L))
    {
        cout << "Ԫ��cur_e�����һ��Ԫ��,û�к���!" << endl;
        exit(1);
    }
    q = q->next;
    return q;
}
