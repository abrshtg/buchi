from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_generate_report():
    response = client.get("/api/v1/generateReport",
                          params={'fromDate': '2023-02-02', 'toDate': '2023-03-03'})

    assert response.status_code == 200
    # assert response.json() == {
    #     "status": "success",
    #     "data": {
    #         "adoptedPetTypes": {
    #             "dog": 8,
    #             "cat": 1,
    #             "horse": 3
    #         },
    #         "weeklyAdoptionRequests": {
    #             "2023-01-30": 0,
    #             "2023-02-06": 0,
    #             "2023-02-13": 5,
    #             "2023-02-20": 7,
    #             "2023-02-27": 0
    #         }
    #     }
    # }
