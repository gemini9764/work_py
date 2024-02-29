from array import array
import reprlib
import math
import operator
import functools
import itertools

class Vector:
    typecode = 'd'

    def __init__(self, components):
        #'protected' 객체 속성 self._component는 벡터 요소를 배열로 저장
        self._components = array(self.typecode, components)

    def __iter__(self):
        #반복할 수 있도록 self._components의 반복자를 반환
        return iter(self._components)
    
    def __repr__(self):
        #self._components를 제한된 길이로 표현하기 위해 reprlib.repr()를 사용
        #array('d', [0.0, 1.0, ...]) 형태로 출력
        components = reprlib.repr(self._components)
        #문자열을 Vector 생서자에 전달할 수 있도록 문자열 "array('d', "와
        #마지막 괄호를 제거
        components = components[components.find('['):-1]
        return f'Vecotor({components})'
    
    def __str__(self):
        return str(tuple(self))
    
    def __bytes__(self):
        return (bytes([ord(self.typecode)])) + bytes(self._components)  #self._components에서 바로 bytes 객체 생성
    
    def __eq__(self, other):
        return (len(self) == len(other) and all(a==b for a, b in zip(self, other)))

    def __hash__(self):
        #각 요소의 해시를 계산하기 위한 제너레이터 표현식을 생성
        hashes = (hash(x) for x in self._components)
        #xor 함수와 hashes를 전달하여 reduce() 함수 호출, 세번째 인수 0은 초기값
        return functools.reduce(operator.xor, hashes, 0)
    
    def __abs__(self):
        #파이썬 3.8부터 math.hypot은 n차원 포인트를 받을 수 있음, 파이썬 3.8 이전이라면
        #math.sqrt(sum(x*x for x in self))로 작성
        return math.hypot(*self)
    
    def __bool__(self):
        return bool(abs(self))
    
    def __len__(self):
        return len(self._components)
    
    def __getitem__(self, key):
        if isinstance(key, slice):  #if index's type is slice
            #객체의 클래스(Vector)를 가져옴
            cls = type(self)
            #_components 배열의 슬라이스로부터 Vector 객체 생성
            return cls(self._components[key])
        #if index's type is Integral
        index = operator.index(key)
        #_components에서 해당 항목을 가져와서 반환
        return self._components[index]
    
    #__getattr__에 의해 지원되는 dynamic attributes의 매칭 패턴
    __match_args__ = ('x', 'y', 'z', 't')

    def __getter__(self, name):
        #Vector 클래스를 가져옴
        cls = type(self)
        try:
            #__match_args__에서 name의 위치를 가져옴
            pos = cls.__match_args__.index(name)
        #name을 찾지 못했을 때, .index(name)는 ValueError를 발생시킴
        except ValueError:
            #name을 찾미 못하면 pos를 -1로 설정
            pos = -1
        #pos가 유효한 인덱스라면 해당 항목 반환
        if 0 <= pos < len(self._components):
            return self._components[pos]
        #여기까지 도달하면 문제가 발생했다는 것이고, AttributeError를 발생시킴
        msg = f'{cls.__name__!r} object has no attirbute {name!r}'
        raise AttributeError(msg)
    
    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            if name in cls.__match_args__:
                error = 'readonly attribute {attr_name!r}'
            elif name.islower():
                error = "can't set attribute 'a' to 'z' in {cls_name!r}"
            else:
                error = ''
            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
            super().__setattr__(name, value)

    #특정 좌표에 대한 각좌표를 계산
    def angle(self, n):
        r = math.hypot(*self[n:])
        a = math.atan2(r, self[n-1])
        if (n == len(self - 1) and (self[-1] < 0)):
            return math.pi * 2 - a
        else:
            return a
        
    #모든 각좌표를 계산하는 제너레이터 표현식을 생성
    def angles(self):
        return (self.angle(n) for n in range(1, len(self)))
    
    def __format__(self, fmt_spec=''):
        if fmt_spec.endwidth('h'):
            fmt_spec = fmt_spec[:-1]
            #itertools.chain() 함수를 이용해서 크기와 각좌표를 차례로 반복하는
            #제너레이터 표현식 생성
            coords = itertools.chain([abs(self), self.angles()])
            outer_fmt = '<{}>'  #구면좌표는 꺽쇠괄호를 이용하여 출력
        else:
            coords = selfouter_fmt = '({})' #직교좌표는 괄호를 이용하여 출력
        #좌표의 각 항목을 요구사항에 따라 포맷하는 제너레이터 표현식 생성
        components = (format(c, fmt_spec) for c in coords)
        #포맷된 요소들을 콤마로 분리하여 반환
        return outer_fmt.format(', '.join(components))
    
    #classmethod
    def formbytes(cls, octets):
        typecode = chr(octets[0])  
        memv = memoryview(octets[1:].cast(typecode))
        return cls(memv)    #*를 이용해서 언패킹할 필요없음