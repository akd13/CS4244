#include <stdio.h>
#define red 0
#define green 1
#define white 2
#define blue 3
#define yellow 4 
#define color(x,y) ((x)+5*(y)) 
#define brit 5
#define swede 6
#define dane 7
#define norwegian 8
#define german 9
#define lives(x,y) ((x)+5*(y))
#define tea 10
#define coffee 11
#define water 12
#define beer 13
#define milk 14
#define drinks(x,y) ((x)+5*(y)) 
#define Prince 15
#define Blends 16
#define PallMall 17
#define BlueMaster 18
#define Dunhill 19
#define smokes(x,y) ((x)+5*(y)) 
#define dog 20
#define cat 21
#define bird 22
#define horse 23
#define fish 24
#define pets(x,y) ((x)+5*(y)) 

int main(void) 
{
	freopen("einstein.cnf","w",stdout);
    
	printf("p cnf 125 889\n"); // actual clauses: 889
	int a,b,k;
	for (k = 0; k < 5; k++) 
	{
		// every house has a color
		for (a = 1; a <= 5; a++) 
			printf("%d ", color(a, k));
		printf("0\n");
		
		for (a = 1; a <= 5; a++) 
		{
			for (b = 1; b < a; b++) // a color can be used once
				printf("-%d -%d 0\n", color(a, k), color(b, k));
			for (b = 0; b < 5 ; b++) 
				if (b != k)				// a house can have only one color.
					printf("-%d -%d 0\n", color(a, k), color(a, b));
		}
	}

	for (k = 0; k < 5; k++) 
	{
		// every house has a nationality
		for (a = 1; a <= 5; a++) 
			printf("%d ", lives(a, k)+50);
		printf("0\n");
		
		for (a = 1; a <= 5; a++) 
		{
			for (b = 1; b < a; b++) // a nationality can be used once
				printf("-%d -%d 0\n", lives(a, k)+50, lives(b, k)+50);
			for (b = 0; b < 5 ; b++) 
				if (b != k)				// a house can have only one nationality.
					printf("-%d -%d 0\n", lives(a, k)+50, lives(a, b)+50);
		}
	}


	for (k = 0; k < 5; k++) 
	{
		// every house has a drink
		for (a = 1; a <= 5; a++) 
			printf("%d ", drinks(a, k)+75);
		printf("0\n");
		
		for (a = 1; a <= 5; a++) 
		{
			for (b = 1; b < a; b++) // a drink can be used once
				printf("-%d -%d 0\n", drinks(a, k)+75, drinks(b, k)+75);
			for (b = 0; b < 5 ; b++) 
				if (b != k)				// a house can have only one drink.
					printf("-%d -%d 0\n", drinks(a, k)+75, drinks(a, b)+75);
		}
	}


	for (k = 0; k < 5; k++) 
	{
		// every house has a cigar
		for (a = 1; a <= 5; a++) 
			printf("%d ", smokes(a, k)+100);
		printf("0\n");
		
		for (a = 1; a <= 5; a++) 
		{
			for (b = 1; b < a; b++) // a cigar can be used once
				printf("-%d -%d 0\n", smokes(a, k)+100, smokes(b, k)+100);
			for (b = 0; b < 5 ; b++) 
				if (b != k)				// a house can have only one cigar.
					printf("-%d -%d 0\n", smokes(a, k)+100, smokes(a, b)+100);
		}
	}


	for (k = 0; k < 5; k++) 
	{
		// every house has a pet
		for (a = 1; a <= 5; a++) 
			printf("%d ", pets(a, k)+25);
		printf("0\n");
		
		for (a = 1; a <= 5; a++) 
		{
			for (b = 1; b < a; b++) // a pet can be used once
				printf("-%d -%d 0\n", pets(a, k)+25, pets(b, k)+25);
			for (b = 0; b < 5 ; b++) 
				if (b != k)				// a house can have only one pet.
					printf("-%d -%d 0\n", pets(a, k)+25, pets(a, b)+25);
		}
	}

		// The Brit lives in the red house
		for (a = 1; a <= 5; a++) 
		{
			printf("-%d %d 0\n", lives(a, brit), color(a, red));
			printf("%d -%d 0\n", lives(a, brit), color(a, red));

		}

		// The Swede keeps dogs as pets
		for (a = 1; a <= 5; a++) 
		{
			printf("-%d %d 0\n", lives(a, swede), pets(a, dog));
			printf("%d -%d 0\n", lives(a, swede), pets(a, dog));
		} 

		// The Dane drinks tea
		for (a = 1; a <= 5; a++) 
		{
			printf("-%d %d 0\n", lives(a, dane), drinks(a, tea));
			printf("%d -%d 0\n", lives(a, dane), drinks(a, tea));
		} 

		// The green house is on the left of the white house
		for (a = 1; a <= 5; a++) 
		{
			for(b = 5; b>=1;b--)
			{	
				if((b>=a-1)&&(b<=a))
				{	}
				else
					{printf("-%d -%d 0\n", color(a, white), color(b, green));}
			}  
		}

		//The green house owner drinks coffee
		for (a = 1; a <= 5; a++) 
		{
			printf("-%d %d 0\n", color(a, green), drinks(a, coffee));
			printf("%d -%d 0\n", color(a, green), drinks(a, coffee));
		} 

		//The person who smokes Pall Mall rears birds
		for (a = 1; a <= 5; a++) 
		{
			printf("-%d %d 0\n", smokes(a, PallMall), pets(a, bird));
			printf("%d -%d 0\n", smokes(a, PallMall), pets(a, bird));
		} 

		//The owner of yellow house smokes Dunhill
		for (a = 1; a <= 5; a++) 
		{
			printf("-%d %d 0\n", color(a, yellow), smokes(a, Dunhill));
			printf("%d -%d 0\n", color(a, yellow), smokes(a, Dunhill));
		} 

		// The man living in the center house drinks milk
		printf("%d 0\n", drinks(3, milk));

		// The Norwegian lives in the first house
		printf("%d 0\n", lives(1, norwegian)); 

		// The man who smokes Blends lives next to the one who keeps cats
		printf("-%d %d 0\n", smokes(1, Blends), pets(2, cat));
		printf("-%d %d 0\n", smokes(5, Blends), pets(4, cat));
		
		for (a = 2; a <= 4; a++) 
		{
			printf("-%d %d %d 0\n",smokes(a, Blends),pets(a-1, cat), pets(a+1, cat));
		} 

		// The man who keeps the horse lives next to the one who smokes Dunhill
		printf("-%d %d 0\n", pets(1, horse), smokes(2, Dunhill));
		printf("-%d %d 0\n", pets(5, horse), smokes(4, Dunhill));
		
		for (a = 2; a <= 4; a++) 
		{
			printf("-%d %d %d 0\n",pets(a, horse),smokes(a-1, Dunhill), smokes(a+1, Dunhill));
		} 

		//The owner who smokes BlueMaster drinks beer.
		for (a = 1; a <= 5; a++) 
		{
			printf("-%d %d 0\n", smokes(a, BlueMaster), drinks(a, beer));
			printf("%d -%d 0\n", smokes(a, BlueMaster), drinks(a, beer));
		} 

		// The German smokes Prince
		for (a = 1; a <= 5; a++) 
		{
			printf("-%d %d 0\n", lives(a, german), smokes(a, Prince));
			printf("%d -%d 0\n", lives(a, german), smokes(a, Prince));
		} 

		// The Norwegian lives next to the blue house
		printf("%d 0\n", color(2, blue)); 

		// The man who smokes Blends has a neighbour who drinks water
		printf("-%d %d 0\n", smokes(1, Blends), drinks(2, water));
		printf("-%d %d 0\n", smokes(5, Blends), drinks(4, water));
		
		for (a = 2; a <= 4; a++) 
		{
			printf("-%d %d %d 0\n",smokes(a, Blends),drinks(a-1, water), drinks(a+1, water));
		} 

	
		return 0;
}
