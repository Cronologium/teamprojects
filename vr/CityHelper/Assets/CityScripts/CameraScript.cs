using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class CameraScript : MonoBehaviour {

    public float moveSpeed = 15f;
    public bool playerIsDead = false;
    private GameObject lookAtTarget;
    private Camera camera;

    private void Start()
    {
        camera = GetComponentInChildren<Camera>();
    }

    void Update()
    {
        if (playerIsDead)
        {
            if (lookAtTarget != null)
                transform.LookAt(lookAtTarget.transform);
            return;
        }

        // use camera's rotation for deciding what's forward
        if (camera != null)
        {
            transform.position += new Vector3(camera.transform.forward.x, 0, camera.transform.forward.z) * Input.GetAxis("Vertical") * moveSpeed * Time.deltaTime;
            transform.position += new Vector3(camera.transform.right.x, 0, camera.transform.right.z) * Input.GetAxis("Horizontal") * moveSpeed * Time.deltaTime;
        }
    }

    public void OnBodyCollided(GameObject lookAtObject)
    {
        playerIsDead = true;
        Time.timeScale = 0.5f;
        Invoke("ResetGame", 2f);

        Vector3 savePos = transform.position;
        Vector3 pos = transform.position;
        pos.y += 10f; // move it upwards
        pos += new Vector3(camera.transform.forward.x, 0, camera.transform.forward.z) * -30f; // and backwards
        transform.position = pos;

        transform.LookAt(lookAtObject.transform);
        lookAtTarget = lookAtObject;
    }

    void ResetGame()
    {
        Time.timeScale = 1f;
        SceneManager.LoadScene(SceneManager.GetActiveScene().name);
        playerIsDead = false;
    }
}
