using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarGeneratorScript : MonoBehaviour {

    public string direction;

    // Use this for initialization
    void Start () {

    }

    // Update is called once per frame
    void Update () {

    }

    public void Generate()
    {
        Vector3 rotation = new Vector3();
        Vector3 startForce = GameManager.instance.GetForceVectorForDirection(direction);
        if (direction == "x+")
            rotation.y = 180f;
        if (direction == "z-")
            rotation.y = 270f;
        if (direction == "z+")
            rotation.y = 90f;

        GameObject gobj = Instantiate(GameManager.instance.carPrefabs[Random.Range(0, GameManager.instance.carPrefabs.Length)], gameObject.transform.position, Quaternion.identity);
        gobj.transform.eulerAngles = rotation;
        gobj.GetComponent<Rigidbody>().AddForce(startForce);
        gobj.GetComponent<CarScript>().direction = direction;
        GameManager.instance.spawnedCars.Add(gobj);
    }
}
