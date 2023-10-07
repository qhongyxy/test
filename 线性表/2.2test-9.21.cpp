#include <iostream>
#include "function_list_Sq.cpp"
using namespace std;
int main()
{
    List_Sq la,lb;
    InitList_Sq(la);
    InitList_Sq(lb);
    cout << "************* Input A ***************" << endl;
    putq(la);
    cout << "************* Input B ***************" << endl;
    putq(lb);
    cout <<endl<< "************* Result ****************" << endl;
    cout << "A = ";
    ListTraverse(la);
    cout << "B = ";
    ListTraverse(lb); 
    List_Sq ld;
    ld = addictation_List_Sq(la, lb);
    ListTraverse(ld);
    List_Sq lc;
    lc = Intersection_List_Sq(la, lb);
    ListTraverse(lc);
    List_Sq le;
    le = subtraction_List_Sq(la, lb);
    cout << "A - B = ";
    ListTraverse(le);
    List_Sq lf;
    lf = subtraction_List_Sq(lb, la);
    cout << "B - A = ";
    ListTraverse(lf);
    cout << "**************************************" << endl;
    system("pause");
    return 0;
}