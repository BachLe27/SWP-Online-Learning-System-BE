if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="api.v1:app", host="0.0.0.0", port=8000, debug=True, reload=True)
