# Melange 모듈 개발 가이드 (python)

## Clone

```
git clone https://github.com/Mino-is-me/Melange.git
```

## Branch
1. main 
2. dev/lib 
    * 라이브러리 차력쇼 
3. feature/[feature - name]
    * 특정 피쳐 개발
## 프로젝트 경로

`//CINEVStudio/Content/Python/` 

## 알아둘 점

폴더를 Module로 사용하실거라면 (Lib처럼) 꼭 __init__ 파일을 만들어주셔야합니다. 

## 코드 작성 규약 
**Type Hinting 꼭 해주세요**

## IDE 세팅

* **VSCODE 쓰세요** 

### 필수 익스텐션
* **Unreal Engine Python**
1. Code에서 Unreal Attach 걸어서 런타임 디버깅 가능하게 해줍니다, 꼭 설치해주세요, 나머지는 편한대로 
----

# 라이브러리 설명

라이브러리 만든 사람 취향에 따라 스타레일 캐릭터 이름이 되었습니다(…)

## Topaz

`\CINEVStudio\Content\Python\Lib\__lib_topaz__.py`

Asset / Actor 등 [언리얼 에디터 안에서] 컨트롤 할 수 있는 자산들에 대한 다방면의 함수를 제공합니다.

예를 들어 클릭한 액터/어셋만 list로 리턴한다던가…블루프린트 컴포넌트를 클래스에 맞게 긁어준다던가…

엥간한 함수가 다 있으니, 웬만하면 임포트 하고 시작하는것도 좋습니다. 

## Stelle

`\CINEVStudio\Content\Python\Lib\__lib_stelle__.py`

스텔레는 역으로 어셋/액터가 아니라 CSV 파싱 /  쓰기나 익스포트 등 [언리얼 에디터 밖에서] 할 수 있는 일들에 초점이 맞춰져 있습니다, 스텔레에서도 토파즈를 임포트해서 사용합니다. 

## Archeron

`\CINEVStudio\Content\Python\Lib\__lib_archeron__.py`

아케론은 대량 작업에 초점이 맞춰져 있습니다, 레벨에 배치된 인스턴스를 죄다 긁어서 셋업된 조건에 따라 다운사이징 한다던가 하는 등입니다.

## Himeko 

`\CINEVStudio\Content\Python\Lib\__lib_himeko__.py`


## 라이브러리는 아닌데 참고하면 좋은 것

### 스파클

`\CINEVStudio\Content\Python\Sparkle.py`

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

