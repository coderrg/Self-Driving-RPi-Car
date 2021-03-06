# Big Picture Summary
  Autonomous vehicles are revolutionizing people’s daily lives, but there are still major challenges these vehicles face. One of the biggest problems they have is accurately determining the edges of the path they are traveling on across various conditions. In this project, a robust system for determining the edges of the path in an input image was developed and then deployed on a Raspberry Pi-based autonomous vehicle model to test its effectiveness.
# The Goal
  The engineering goal of creating a more robust path edge determination algorithm was achieved in this project, and the expected outcome of creating a model Raspberry Pi-based autonomous vehicle that can navigate an unmarked path using only input image data was also finished. Namely, Algorithm 4 (the final algorithm), which used a convolutional neural network and computer vision, had an overall performance score of 990.54 out of a possible 1000 points. This score was determined using three theoretical performance measures and a practical performance measure. The theoretical performance measures tested the accuracy of the predicted left edge, the predicted right edge, and the predicted average slope of the two edges. The practical performance measure tested the accuracy of a model Raspberry-Pi autonomous vehicle navigating a path using the algorithm. Hence, the high overall performance score of Algorithm 4 indicates that it was extremely successful in both the theoretical performance measures and the practical performance measures, so it could potentially be deployed in a real-life scenario.
# Finding the Best Solution
  However, in order to to determine that Algorithm 4 was the optimal solution for the problem at hand, alternate solutions were developed as well and compared to each other. In addition, there were three different paths created with different shapes, angles, and curvatures in order to model different conditions an autonomous vehicle might encounter in real life. There were four algorithms created (Algorithm 1, Algorithm 2, Algorithm 3, Algorithm 4), and the theoretical performance measures and the practical performance measure were used to determine the best algorithm for the task. 
  
 # Theoretical and Practical Performance measures
  The theoretical performance measures were evaluated for each of the algorithms for each of the three paths. In each of the three paths, Algorithm 4 came out as the most successful with the highest overall theoretical accuracy, When the overall theoretical accuracy scores were averaged for each of the three paths, the overall theoretical performance scores out of 1000 for Algorithm 1, Algorithm 2, Algorithm 3, and Algorithm 4 were 756.76, 935.59, 968.89, and 997.38, respectively. As a result, the theoretical data proved that the accuracy of Algorithm 4 in determining the correct edges of the path was the best among all the algorithms. 
The practical performance measure was evaluated for each of the algorithms five times for five trials. The average percentages of time that the model Raspberry-Pi autonomous vehicle stayed on the path for Algorithm 1, Algorithm 2, Algorithm 3, and Algorithm 4 were 64.82%, 78.15%,  91.63%, and 98.37%, respectively. Therefore, it was shown that practically, when each of the algorithms was deployed on an actual autonomous vehicle, Algorithm 4 was most successful, implying that Algorithm 4 was the most consistent and precise when it came to predicting the edges of a path.
# Overall Peformance
  After collecting all the data, the overall performance scores (the average of the practical numeric percentage times 10 (e.g. 75% x 10 = 750) and the theoretical score) came out to be 702.48, 858.55, 942.60, and 990.54 out of 1000 for Algorithm 1, Algorithm 2, Algorithm 3, and Algorithm 4, respectively, proving how Algorithm 4 was the best overall algorithm.
# Final Product
In conclusion, the final product created out of this project was a Raspberry-Pi autonomous vehicle that used Algorithm 4 to accurately and consistently detect the edges of the path and thus navigate the path, regardless of the shape of the path. Hence, the engineering goal was met.
# Credits
The basic dataset for this project came from https://github.com/mvirgo/MLND-Capstone/, although the images in the dataset were significantly modified for the purpose of this project. Michael Virgo's project was beneficial to me in elements of this project such as the creation of the convolutional neural network. A big thanks to him.

Here is his MIT License.

MIT License

Copyright (c) 2017 Michael Virgo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
