using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class CarTriggerScript : MonoBehaviour {

    public GameObject carGenerator;

    // Use this for initialization
    void Start () {

    }
    
    // Update is called once per frame
    void Update () {

    }

    void OnTriggerEnter(Collider other) {
        GameManager.instance.spawnedCars.Remove(other.gameObject);
        Destroy(other.gameObject);
        carGenerator.GetComponent<CarGeneratorScript>().Generate();
    }
}
