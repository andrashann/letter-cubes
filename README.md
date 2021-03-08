# Words in letter blocks

If you have ever found some wooden blocks with letters on them
and tried to figure out what words you can make using these cubes, look no further
because this is the project to solve your problems.

Is it unclear what I mean? Just look at this picture:

![a photo of three wooden cubes with different letters on each face](og.jpg)

There is an [API](https://letter-blocks.herokuapp.com/) as well as [a simple front end](http://hann.io/words-in-letter-blocks) (which uses the same API).

Why did I do this? When I visited my mother, we found these old wooden blocks with a letter on each face (see the photo above) and wondered what words we could make using them. Programming is sometimes easier than thinking, so I wrote a script to answer this question.

The API uses .dic files from the [LibreOffice GitHub repository](https://github.com/LibreOffice/dictionaries); I do not take responsibility for the words actually being correct or used in daily life. Some of them might not make sense (as this data source is not an actual word list but a source for a spell checker), but most of them should.