# Rich Or Not

## Background

Project Initial Reference [Here](https://github.com/0mgABear/CS50P/tree/main/Week9/final%20project)

In the initial iteration of the project, I had detailed the use case of this project, initial APIs used, limitations and future work.
Please refer here [Here](https://github.com/0mgABear/CS50P/blob/main/Week9/final%20project/README.md)

---

## Key Recap of Project

1. For any finanical firms / "advisors" that are providing sales services, it is useful to determine their potential client's net worth.
   One common way to do so in Singapore is by evaluating their area of residence, as properties in prime areas command a higher intrinsic value, and accordingly may translate to a higher net worth.

2. V1 was a pure CLI only tool , which is not helpful to the vast majority of people, especially non-programmers.

3. V1 was strictly using only OneMap API results, which is insufficient to draw conclusions.

## Key Enhancements in this Iteration:

1. Accurate classification of whether someone stays in public vs private housing. Classification as such - HDB: Public, everything else: Private

How this is achieved:
API calls to the relevant data.gov.sg dataset, in this instance the all HDB building [dataset](https://data.gov.sg/datasets?sort=downloadsCount&query=hdb&resultId=d_17f5382f26140b1fdae0ba2ef6239d2f). Checks is performed against this existing database.

If a record is found, the building is classified as public.

2. Checking of last-transacted price of the postal code.

How this is achieved: API call to relevant datasets (five used here). The datasets are arranged chronologically (latest first), and going back all the way to 1990. If a postal has been determined to be public, it will be checked for their resale value as well. This resale value will be displayed in the final UI output.

For private properties, another alternative URA [dataset](https://eservice.ura.gov.sg/maps/api/#private-residential-property-transactions) is used.

## Key Achivements:

1. This accurately solves the classification problem faced earlier in V1 (the CLI-only solution) without storing data anywhere.
2. This gets the latest transacted price accurately.
3. This functionality is presented in a user friendly site, where anyone can use without the need for programming knowledge, achieving ease of accessibility.

## Key Limitations:

1. Private properties may not be transacted as regularly, so the net-worth of the client will not be shown in the final UI display, due to a lack of data in the URA database.

# Concluding Words:

This was a project initially spurred by a groupmate in my traineeship program, and he was in another financial institution. He lamented how there was no such solution, and I decided to do this as a bet (at the cost of lunch). I won the bet and a free lunch but still decided to develop this further.

Sometimes project ideas can come from the most random of places, but never let that stop you!

This is proudly a @commonertech product.
