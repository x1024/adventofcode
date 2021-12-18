#include <stdio.h>
int main() { int a,b,c,d;a=b=c=d=0;
L1:a=1;
L2:b=1;
L3:c=1;
L4:d=26;
L5:if(c!=0) goto L7;
L6:if(1!=0) goto L11;
L7:c=7;
L8:++d;
L9:--c;
L10:if(c!=0) goto L8;
L11:c=a;
L12:++a;
L13:--b;
L14:if(b!=0) goto L12;
L15:b=c;
L16:--d;
L17:if(d!=0) goto L11;
L18:c=18;
L19:d=11;
L20:++a;
L21:--d;
L22:if(d!=0) goto L20;
L23:--c;
L24:if(c!=0) goto L19;
printf("%d\n",a); }
