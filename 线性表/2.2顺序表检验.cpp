#include <iostream>
#include "function_list_Sq.cpp"
using namespace std;
int main()
{
    List_Sq la,lb,lc;
   //  int g,l,m; 
    InitList_Sq(la);
    InitList_Sq(lb);
    InitList_Sq(lc);
   
    putp(la);
    putp(lb);
    //��ѯԪ��
      //  ElemType d,e,f;
    // cout << "��������Ҫ��ѯ��Ԫ��:" << endl;
    // cin >> d;
    
   //���˳�����
    // g = LocateElem(la, d);
    // cout << "la��˳�����:" << la.length << endl;

    // cout << "��Ҫ���ҵ�Ԫ�ص�λ��:" << g << endl;

    // cout << "��������Ҫɾ����Ԫ�ص�λ��:" << endl;
    // cin >> l;
    // ListDelete(la,l,e);
    // ListTraverse(la);
    // cout << "la��˳�����:" << la.length << endl;

    // cout << "��������Ҫ�����Ԫ��:" << endl;
    // cin >> f;
    // cout << "��������Ҫ������ĸ�λ��Ԫ��֮ǰ:" << endl;
    // cin >> m;
   //  ListInsert(la, m, f);
   //  ListTraverse(la);
       lc=Intersection_List_Sq(la, lb);
       ListTraverse(lc);
    
       List_Sq ld;
       InitList_Sq(ld);
          ld = addictation_List_Sq(la, lb);
          ListTraverse(ld);
        List_Sq le;
       InitList_Sq(le);
          le = subtraction_List_Sq(la, lb);
          ListTraverse(le);
          List_Sq lf;
       InitList_Sq(lf);
          lf = subtraction_List_Sq(lb, la);
          ListTraverse(lf);
       system("pause");
       return 0;
}