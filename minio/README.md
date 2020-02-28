docker run -v -v `pwd`/minio/data:/data -e "MINIO_ACCESS_KEY=minio" -e "MINIO_SECRET_KEY=minio1234" -p 9000:9000 minio/minio server /data
