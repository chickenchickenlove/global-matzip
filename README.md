# global-matzip
- 이 파이썬 스크립트는 `Google Map API`의 `PlacesAPI`를 이용해 특정 지역의 식당 정보를 수집합니다. 
- 가져온 정보는 <현재날짜 + 시간(분초)>-<도시이름>-<랜덤 UUID> 디렉토리 아래에 생성됩니다.
- 각 파일의 한 줄은 <식당명>/<주소>/<평점> 입니다.

### Run
```shell
$ python google_information_getter.py <config_file_path>
```

### Caution
- 구글 지도 API의 Nearby Search를 사용합니다.
- 이 요청은 23년 8월 기준 32불 / 1,000회의 비용이 청구됩니다.
- 무료 체험 계정일 경우 200불의 크레딧이 주어진다고 합니다.
- https://developers.google.com/maps/billing/gmp-billing?hl=ko
- nearbySeach api billing : 32$ / 1000
![img.png](img.png)


### Config 파일
- `diameter` : 구역을 나눌 직경. 
- `city` : 검색할 도시. position_constant에 있는 값입니다. 
- `find_type` : 검색할 타입. 
- `is_async` : False / True. Async로 할 경우, 이벤트 루프에서 멀티 프로세싱 처리되어 좀 더 빠른 결과를 기대할 수 있습니다. 
```yaml
google:
  api_key: <YOUR_API_KEY>
search:
  diameter: 25000
  city:
    - BALI
    - HANOI
  find_type: restaurant
is_async: False

```

### 도시 추가하는 방법
- git clone 후, position_constant.py 파일에 양식에 맞게 도시 + 좌표를 추가하세요.

