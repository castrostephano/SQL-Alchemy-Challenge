{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 1. import Flask (makes it a webpage)\n",
    "\n",
    "\n",
    "from flask import Flask\n",
    "\n",
    "# 2. Create an app, being sure to pass __name__ _ _ means initalizing a class\n",
    "app = Flask(__name__)\n",
    "\n",
    "\n",
    "# 3. Define what to do when a user hits the index route\n",
    "@app.route(\"/api/v1.0/precipitation\")\n",
    "def home():\n",
    "    print(\"Server received request for 'Home' page...\")\n",
    "    return \"Welcome to my 'Home' page!\"\n",
    "\n",
    "\n",
    "# 4. Define what to do when a user hits the /about route\n",
    "@app.route(\"/about\")\n",
    "def about():\n",
    "    print(\"Server received request for 'About' page...\")\n",
    "    return \"Welcome to my 'About' page!\"\n",
    "\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    app.run(debug=True)\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
