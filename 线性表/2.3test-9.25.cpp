#include <iostream>
#include "Link_List.cpp"
using namespace std;
int main()
{
    LinkList la,lb;
    cout << "************* Input A ***************" << endl;
    putq(la);
    cout << "************* Input B ***************" << endl;
    putq(lb);
    cout <<endl<< "************* Result ****************" << endl;
    cout << "A = ";
    Traverse_ListLink(la);
    cout << "B = ";
    Traverse_ListLink(lb); 
    LinkList ld;
    ld = and_LinkList(la, lb);
    Traverse_ListLink(ld);
    LinkList lc;
    lc = Intersection_LinkList(la, lb);
    Traverse_ListLink(lc);
    LinkList le;
    le = subtraction_LinkList(la, lb);
    cout << "A - B = ";
    Traverse_ListLink(le);
    LinkList lf;
    lf = subtraction_LinkList(lb, la);
    cout << "B - A = ";
    Traverse_ListLink(lf);
    cout << "**************************************" << endl;
    system("pause");
    return 0;
}