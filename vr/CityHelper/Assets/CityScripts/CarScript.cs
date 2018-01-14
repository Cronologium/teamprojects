using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarScript : MonoBehaviour {

    bool isWaiting = false;
    public string direction;

    bool isCarOnTheOppositeLane(GameObject gobj)
    {
        return gobj.GetComponent<CarScript>().direction[0] == direction[0] && gobj.GetComponent<CarScript>().direction[1] != direction[1];
    }

    void FixedUpdate()
    {
        if (direction != "x-" && direction != "x+")
            return;

        if (isWaiting)
        {
            bool hasNearbyObject = false;
            foreach (GameObject gobj in GameManager.instance.spawnedCars)
            {
                if (gobj == gameObject)
                    continue;

                if (Vector3.Distance(gameObject.transform.position, gobj.transform.position) < 30f && !isCarOnTheOppositeLane(gobj))
                {
                    hasNearbyObject = true;
                    break;
                }
            }

            if (!hasNearbyObject)
            {
                isWaiting = false;
                Vector3 startForce = GameManager.instance.GetForceVectorForDirection(direction);
                gameObject.GetComponent<Rigidbody>().AddForce(startForce);
                return;
            }
        }

        foreach (GameObject gobj in GameManager.instance.spawnedCars)
        {
            if (gobj == gameObject)
                continue;

            if (Vector3.Distance(gameObject.transform.position, gobj.transform.position) < 30f && !isCarOnTheOppositeLane(gobj))
            {
                isWaiting = true;
                gameObject.GetComponent<Rigidbody>().velocity = Vector3.zero;
                return;
            }
        }
    }
}
