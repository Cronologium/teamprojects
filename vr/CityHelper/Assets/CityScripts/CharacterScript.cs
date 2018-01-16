using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CharacterScript : MonoBehaviour {

    Vector3 position;
    public GameObject player;

    private void Awake()
    {
        position = transform.position;

        Renderer[] renderers = gameObject.GetComponentsInChildren<Renderer>();
        foreach (Renderer renderer in renderers)
            renderer.enabled = false;
    }

    private void LateUpdate()
    {
        CameraScript cs = player.GetComponent<CameraScript>();
        if (cs == null || cs.playerIsDead)
            return;

        Vector3 lockedX = player.transform.eulerAngles;
        lockedX.x = 0;
        transform.eulerAngles = lockedX;

        //transform.position = position;
        if (player != null)
            transform.position = player.transform.position - new Vector3(0, 6.7f, 0);
    }

    private void OnCollisionEnter(Collision collision)
    {
        CameraScript cs = player.GetComponent<CameraScript>();
        if (cs != null)
        {
            Renderer[] renderers = gameObject.GetComponentsInChildren<Renderer>();
            foreach (Renderer renderer in renderers)
                renderer.enabled = true;

            cs.OnBodyCollided(gameObject);
        }

        Rigidbody rb = GetComponent<Rigidbody>();
        if (rb != null && collision.gameObject.name.Equals("SwimmingPoolWater"))
            rb.useGravity = true;
    }
}
