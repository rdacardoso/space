#ALG_PACK.PY

#contem as seguintes classes:
#Matrix33
#Vector3

import math

class Matrix33(object):
       #atributos:
       #                    |  m00   m01  m02   |
       #m[3][3]   =    | m10     m11 m12   |
       #                    |  m20    m21  m22  |  

       def __init__( self, m00, m01, m02, m10, m11, m12, m20, m21, m22 ):
              mm = [ [m00,m01,m02],[m10,m11,m12],[m20,m21,m22]]
              self.m = mm

       def setValor(self, val, i, j):
              if ((i>=0) and (i<=2)) and ((j>=0) and (j<=2)):
                     self.m[i][j] = val

       def getIJ(self, i, j):
              return self.m[i][j]

       def somaMatrix33(self, g):
              ret =Matrix33(0,0,0,0,0,0,0,0,0)
              for i in range(0,3):
                     for j in range(0,3):
                            f = self.m[i][j]+g.getIJ(i,j)
                            ret.setValor(f,i,j)
              return ret

       def subtraiMatrix33(self,g):
              ret =Matrix33(0,0,0,0,0,0,0,0,0)
              for i in range(0,3):
                     for j in range(0,3):
                            f = self.m[i][j]-g.getIJ(i,j)
                            ret.setValor(f,i,j)
              return ret

       def multiplicaMatrix33(self,g):
              ret =Matrix33(0,0,0,0,0,0,0,0,0)
              for i in range(0,3):
                     for j in range(0,3):
                            f = self.m[i][j]*g.getIJ(i,j)
                            ret.setValor(f,i,j)
              return ret

       def somaComMatrix33(self, g):
              for i in range(0,3):
                     for j in range(0,3):
                            f = self.m[i][j]+g.getIJ(i,j)
                            self.setValor(f,i,j)

       def subtraiComMatrix33(self,g):
              for i in range(0,3):
                     for j in range(0,3):
                            f = self.m[i][j]-g.getIJ(i,j)
                            self.setValor(f,i,j)

       def multiplicaComMatrix33(self,g):
              for i in range(0,3):
                     for j in range(0,3):
                            f = self.m[i][j]*g.getIJ(i,j)
                            self.setValor(f,i,j)

       def somaValor(self, val):
               for i in range(0,3):
                     for j in range(0,3):
                            f = self.m[i][j]+val
                            self.setValor(f,i,j)

       def subtraiValor(self,val):
              for i in range(0,3):
                     for j in range(0,3):
                            f = self.m[i][j]-val
                            self.setValor(f,i,j)

       def multiplicaValor(self,val):
              for i in range(0,3):
                     for j in range(0,3):
                            f = self.m[i][j]*val
                            self.setValor(f,i,j)

       def divideValor(self,val):
              if (val != 0.0):
                     for i in range(0,3):
                            for j in range(0,3):
                                   f = self.m[i][j]/val
                                   self.setValor(f,i,j)
              else:
                     print("Divisão por Zero")

       def setM(self, m00, m01, m02, m10, m11, m12, m20, m21, m22 ):
              mm = [ [m00,m01,m02],[m10,m11,m12],[m20,m21,m22]]
              self.m = mm

       def zera(self):
              for i in range(0,3):
                     for j in range(0,3):
                            self.setValor(0.0,i,j)

       def identidade(self):
               for i in range(0,3):
                     for j in range(0,3):
                            if (i==j):
                                   self.setValor(1.0,i,j)
                            else:
                                   self.setValor(0.0,i,j)

       def transposta(self):
               ret =Matrix33(0,0,0,0,0,0,0,0,0)
               for i in range(0,3):
                      for j in range(0,3):
                             ret.setValor(self.m[i][j],j,i)
               for i in range(0,3):
                      for j in range(0,3):
                             self.setValor(ret.getIJ(i,j),i,j)

       def determinante(self):
              ret =Matrix33(0,0,0,0,0,0,0,0,0)
              ret = self.m[0][0]*self.m[1][1]*self.m[2][2]+self.m[0][1]*self.m[1][2]*self.m[2][0]
              +self.m[0][2]*self.m[1][0]*self.m[2][1]-self.m[0][2]*self.m[1][1]*self.m[2][0]
              -self.m[0][1]*self.m[1][0]*self.m[2][2]-self.m[0][0]*self.m[1][2]*self.m[2][1]
              return ret

       def imprimeMatriz(self):
              for i in range(0,3):
                     print("\n\t%5.3f\t%5.3f\t%5.3f"%(self.getIJ(i,0), self.getIJ(i,1), self.getIJ(i,2)))
              
class Vector3(object):
       #atributos:
       # v[3]   -> [ x , y , z ]
       
       def __init__(self,x,y,z):
              vv = [x,y,z]
              self.v = vv
              
       def VxVyVz(self,x,y,z):
              vv = [x,y,z]
              self.v=vv

       def VX(self):
              return self.v[0]

       def VY(self):
              return self.v[1]

       def VZ(self):
              return self.v[2]

       def setVX(self, v):
              self.v[0] = v

       def setVY(self, v):
              self.v[1] = v

       def setVZ(self, v):
              self.v[2] = v

       def VI(self,i):
              if (i>=0) and (i<=2):
                     return self.v[i]
              else:
                     return 0
       def somaVetor(self, vec):
              vRet = Vector3(0.0,0.0,0.0)
              for i in range(0,3):
                     vRet.v[i]=self.v[i]+vec.v[i]
              return vRet

       def subtraiVetor(self, vec):
              vRet = Vector3(0.0,0.0,0.0)
              for i in range(0,3):
                     vRet.v[i]=self.v[i]-vec.v[i]
              return vRet

       def multiplicaVetor(self, vec):
              vRet = Vector3(0,0,0)
              for i in range(0,3):
                     vRet.v[i]=self.v[i]*vec.v[i]
              return vRet

       def somaComVetor(self,vec):
              for i in range(0,3):
                     self.v[i]=self.v[i]+vec.v[i]

       def subtraiComVetor(self,vec):
               for i in range(0,3):
                     self.v[i]=self.v[i]-vec.v[i]

       def multiplicaComVetor(self,vec):
              for i in range(0,3):
                     self.v[i]=self.v[i]*vec.v[i]

       def somaValor(self,val):
              vRet = Vector3(0.0,0.0,0.0)
              for i in range(0,3):
                     vRet.v[i]=self.v[i]+val
              return vRet

       def subtraiValor(self,val):
              vRet = Vector3(0.0,0.0,0.0)
              for i in range(0,3):
                     vRet.v[i]=self.v[i]-val
              return vRet

       def multiplicaValor(self,val):
              vRet = Vector3(0.0,0.0,0.0)
              for i in range(0,3):
                     vRet.v[i]=self.v[i]*val
              return vRet

       def divideValor(self,val):
              vRet = Vector3(0.0,0.0,0.0)
              if (val != 0.0):
                     for i in range(0,3):
                            vRet.v[i]=self.v[i]/val
              return vRet

       def zera(self):
              for i in range(0,3):
                     self.v[i]=0.0

       def normaliza(self):
              mod = math.sqrt(self.v[0]*self.v[0] + self.v[1]*self.v[1] + self.v[2]*self.v[2])
              if (mod != 0.0):
                     for i in range(0,3):
                            self.v[i]=self.v[i]/mod

       def modulo(self):
              mod = math.sqrt(self.v[0]*self.v[0] + self.v[1]*self.v[1] + self.v[2]*self.v[2])
              return mod

       def setValor(self, val, i):
              if (i>=0) and (i<=2):
                     self.v[i] = val

       def multMat(self, mat):
              ret = Vector3(0.0,0.0,0.0)
              for i in range(0,3):
                     for j in range(0,3):
                            ret.setValor( ret.VI(i) + mat.m[i][j]*self.v[j], i)
              return ret

       def multMatSelf(self, mat):
              ret = Vector3(0.0,0.0,0.0)
              for i in range(0,3):
                     for j in range(0,3):
                            ret.setValor( ret.VI(i) + mat.m[i][j]*self.v[j], i)
              for i in range(0,3):
                     self.v[i] = ret.v[i]
                     
       def dot(self,vec):
              ret = 0.0
              for i in range(0,3):
                     ret = ret + self.v[i]*vec.v[i]
              return ret

       def angulo(self,vec):
              pEsc = self.dot(vec)
              mod1 = self.modulo()
              mod2 = vec.modulo()
              mod = mod1*mod2
              if (mod != 0.0):
                     dummy = pEsc/mod
              else:
                     dummy = 2.0
              if ((dummy>=-1) and (dummy<=1)):
                     ret = math.acos(pEsc/mod)
              else:
                     ret = 0.0
              return ret

       def prodVet(self,vec):
              ret = Vector3(0,0,0)
              ret.setValor(self.v[1]*vec.v[2] - self.v[2]*vec.v[1],0)
              ret.setValor(self.v[2]*vec.v[0] - self.v[0]*vec.v[2],1)
              ret.setValor(self.v[0]*vec.v[1] - self.v[1]*vec.v[0],2)
              return ret
              
       def imprimeVetor(self):
              print("\n")
              for i in range(0,3):
                     print("v[%d] = %f"%(i,self.v[i]))
              print("\n")
       

       


