---
title: sqlite add/delete/update
author: wiloon
type: post
date: 2012-07-08T06:51:30+00:00
url: /?p=3795
categories:
  - DataBase

---
[java]

package com.db.imgfornote;

import android.content.ContentValues;
  
import android.content.Context;
  
import android.database.Cursor;
  
import android.database.sqlite.SQLiteDatabase;
  
import android.database.sqlite.SQLiteDatabase.CursorFactory;
  
import android.database.sqlite.SQLiteOpenHelper;
  
import android.util.Log;

public class DBHelper extends SQLiteOpenHelper {
   
final private static String mDbName="imgfornote";
   
final private static int mDbVersion=1;
   
private static DBHelper mInstance=null;
   
private final static String mTUserPhoto="UserPhoto";
   
final private static String mCreateSqlForNoteClass="create table if not exists NoteClass(classId integer primary key asc autoincrement,className NVARCHAR(100),rowTime timestamp default (datetime(&#8216;now&#8217;, &#8216;localtime&#8217;)))";
   
final private static String mCreateSqlForUserPhoto="create table if not exists UserPhoto(photoId integer primary key asc autoincrement,photoName VARCHAR(200),userPt VARCHAR(200),title VARCHAR(255),classId integer,content NVARCHAR(250),tag NVARCHAR(200),remark text,status integer default 0,rowTime timestamp default (datetime(&#8216;now&#8217;, &#8216;localtime&#8217;)))";
   
final private static String[] mInsertSqlForNoteClass={"insert into NoteClass(className) values(&#8216;默认分类[私有]&#8217;);","insert into NoteClass(className) values(&#8216;读书笔记[私有]&#8217;);","insert into NoteClass(className) values(&#8216;电子资料[公开]&#8217;);"};
   
private DBHelper(Context context, CursorFactory factory) {
   
super(context, mDbName, factory, mDbVersion);
   
}

public static DBHelper GetInstance(Context context, SQLiteDatabase.CursorFactory factory)
   
{
   
if(mInstance==null){
   
mInstance = new DBHelper(context,factory);
   
}
   
return mInstance;
   
}

@Override
   
public void onCreate(SQLiteDatabase db) {
   
// 创建表
   
db.execSQL(mCreateSqlForNoteClass);
   
db.execSQL(mCreateSqlForUserPhoto);
   
//初始化数据
   
for(int i=0;i<mInsertSqlForNoteClass.length;i++)
   
db.execSQL(mInsertSqlForNoteClass[i]);
   
}

@Override
   
public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
   
// TODO Auto-generated method stub

}

private Cursor ExecSQLForCursor(String sql, String[] selectionArgs){
   
SQLiteDatabase db =getWritableDatabase();
   
Log.i("ExecSQLForCursor",sql);
   
return db.rawQuery(sql, selectionArgs);
   
}
   
private void ExecSQL(String sql){
   
try{
   
SQLiteDatabase db =getWritableDatabase();
   
ExecSQL(sql,db);
   
}catch(Exception e){
   
Log.e("ExecSQL Exception",e.getMessage());
   
e.printStackTrace();
   
}
   
}
   
private void ExecSQL(String sql,SQLiteDatabase db ){
   
try{
   
db.execSQL(sql);
   
Log.i("ExecSQL",sql);
   
}catch(Exception e){
   
Log.e("ExecSQL Exception",e.getMessage());
   
e.printStackTrace();
   
}
   
}
   
//添加照片信息
   
public long InsertUserPhoto(String photoName,String title){
   
SQLiteDatabase db =getWritableDatabase();
   
ContentValues cv = new ContentValues();
   
cv.put("photoName", photoName);
   
cv.put("title", title);
   
return db.insert(mTUserPhoto, null, cv);
   
}
   
//查询照片信息
   
public Cursor SearchPhoto(int row,String sort){
   
Cursor cur = null;
   
try{
   
String ord = (sort==null|| sort.toLowerCase().startsWith("a"))?"asc":"desc";
   
String sql = "select * from UserPhoto order by photoId "+ord;
   
String[] args = {String.valueOf(row)};
   
if(row>0){
   
sql +=" limit ?";
   
}else{
   
args=null;
   
}
   
cur = ExecSQLForCursor(sql,args);
   
}catch (Exception e) {
   
cur = null;
   
Log.e("SearchPhoto Exception",e.getMessage());
   
e.printStackTrace();
   
}
   
return cur;
   
}
   
//修改照片信息
   
public int UpdateUserPhoto(int photoId,int classId,String title,String content, String tag){
   
SQLiteDatabase db =getWritableDatabase();
   
ContentValues cv = new ContentValues();
   
cv.put("classId", classId);
   
cv.put("title", title);
   
cv.put("content", content);
   
cv.put("tag", tag);
   
String[] args = {String.valueOf(photoId)};
   
return db.update(mTUserPhoto, cv, "photoId=?",args);
   
}
   
//删除照片信息
   
public int DeleteUserPhoto(int photoId){
   
SQLiteDatabase db =getWritableDatabase();
   
String[] args = {String.valueOf(photoId)};
   
return db.delete(mTUserPhoto, "photoId=?", args);
   
}
  
}

[/java]