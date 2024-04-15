# Melange 모듈 개발 가이드 (python)

## Melange가 뭔가요? 
Melange는 Cinamon.io 에서 개발 / 서비스 예정인 CINEV Studio의 편한 개발을 위한 \
**Unreal Editor Utility Tool** 입니다. \
해당 Repo 이외에도 In-house에서 관리되는 Editor Utility Widget / Blueprint들이 있지만\
이 Repo에는 Python code들만 버전관리를 하고 있습니다. 

## 왜 Melange 인가요? 

Melange를 In-House 툴로 사용하는 CINEV 프로젝트의 구 프로젝트명이 Spice-Pro 였기 때문입니다. 

**Spice Must Flow**

## Clone

```
git clone https://github.com/Mino-is-me/Melange.git
```

## Branch
1. main 
    * 오너가 급하면 가끔 메인에 밀어넣음
2. dev/module
    * 라이브러리 차력쇼 
3. feature/[feature - name]
    * 특정 피쳐 개발
## 프로젝트 경로

`{Unreal Project Path}/Content/Python/` 

## 알아둘 점

* 폴더를 Module로 사용하실거라면 (Lib처럼) 꼭 __init__ 파일을 만들어주셔야합니다. 
    * 이유 : 언리얼 파이썬 버전이 3.11입니다. 

## 코드 작성 규약 
**Type Hinting 꼭 해주세요**\
    나머지는 자율에 맡기고 있습니다. ~~오너도 가끔 스타일이 바뀜~~

## IDE 세팅

* **VSCODE 쓰세요** \
    * PyCharm등 대체 IDE에서의 호환성을 보장하지 않습니다.

### 필수 익스텐션
* **Unreal Engine Python**

    * VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=NilsSoderman.\
 >VSCode에서 Unreal Editor에 Attach를 걸어서 런타임 디버깅이 가능하게 해줍니다, 없으면 개발이 불가능에 가까워집니다.


# 라이브러리 설명

라이브러리 만든 사람 취향에 따라 스타레일 캐릭터 이름이 되었습니다(…)\
???:아니 라이브러리 이름이 비직관적이면 어떡해요!!!! \
~~알 바 아닙니다~~ 이게 Pythonic 아닌가요? Do you know beautifulsoup? 

## Topaz

`Lib\__lib_topaz__.py`

Asset / Actor 등 [언리얼 에디터 안에서] 컨트롤 할 수 있는 자산들에 대한 다방면의 함수를 제공합니다.

예를 들어 클릭한 액터/어셋만 list로 리턴한다던가…블루프린트 컴포넌트를 찾고싶은 클래스에 맞게 긁어준다던가…

Melange 안에 있는 실제 스크립트들이 가장 많이 사용하는 **코어 라이브러리**입니다.

## Stelle

`Lib\__lib_stelle__.py`

스텔레는 역으로 어셋/액터가 아니라 CSV 파싱 /  쓰기나 익스포트 등 [언리얼 에디터 밖에서] 할 수 있는 일들에 초점이 맞춰져 있습니다, 언리얼과는 환경이 격리되어 있습니다. 

## Archeron

`Lib\__lib_archeron__.py`

아케론은 대량 작업에 초점이 맞춰져 있습니다, 레벨에 배치된 인스턴스를 죄다 긁어서 셋업된 조건에 따라 다운사이징 한다던가 하는 등입니다.

## Himeko 

`Lib\__lib_himeko__.py`

히메코는 Unreal Render Queue를 Remote로 컨트롤해서 Render-Farm 등을 세팅할 수 있는 라이브러리 셋입니다.

## Kafka 
`Lib\__lib_himeko__.py`

카프카는 Unreal Editor에서 Git-LFS를 효과적으로 컨트롤하기 위해서 만들어졌습니다. \
UEGit 플러그인이 야기하는 문제 (Unlock after Push가 되다 말다 함 등)을 효과적으로 해결합니다. \
대부분의 함수는 Git CLI를 Project Root에서 실행하기 위한 함수들입니다.


## 라이브러리는 아닌데 참고하면 좋은 것

### 스파클

`Sparkle/*`

```python
import unreal 

objs : list[object] = unreal.EditorLevelLibrary.get_selected_level_actors()
offset : int = 200
grid_num : int = 3
grid_cnt : int = 1

offset_vector = unreal.Vector(x=0.0, y=0.0, z=0.0)

for obj in objs : 
        current_location = obj.get_actor_location()
        new_loc = current_location + offset_vector
        
        if offset_vector.x >= offset * (grid_num - 1) :
            offset_vector = unreal.Vector(x=0.0, y=offset * grid_cnt, z=0.0)
            grid_cnt += 1
        else :
            offset_vector += unreal.Vector(x=offset, y=0.0, z=0.0)

        obj.set_actor_location(new_loc, 0, 1)
        print(obj.get_actor_location())
```

스파클은 위 코드처럼 python 파일을 바로 Execute 하는게 아니라 

멜란지에서 직접 코드를 사용할 때 사용합니다, 
예를 들어, 위 코드에서의 

1. offset
2. grid_num

는 에디터 상의 멜란지에서 UI에 바인딩되어 사용되기 때문에 파이썬 파일을 바로 실행하는 것이 아니라 언리얼 파이썬 인터프리팅 노드에 옮겨적습니다. 

UI에 밸류 바인딩해서 쓸거면 → 스파클에 넣으면 됩니다. 

---
## 코드 완결성
시간은 없고 악당은 많아서 코드나 함수에 중복이 좀 있습니다.\
시간이 좀 나면 정리할 수 있기를...

# Contact
## Onwer
    Narr : narr@cinamon.io 
### Maintainer
    Deemo : deemo@cinamon.io
### Developers
    Ssony : ssony@cinamon.io

    Evan : evan@cinamon.io